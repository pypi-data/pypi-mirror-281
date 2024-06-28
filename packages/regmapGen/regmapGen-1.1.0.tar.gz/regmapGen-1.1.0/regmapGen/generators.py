#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Output file generators
"""

import os
import json
import yaml
import jinja2
import wavedrom
import subprocess
import shutil
from pathlib import Path
from regmapGen import __version__
from . import utils
from . import config
from .regmap import RegisterMap
from .xls_parser import XLSParser, get_bit_reset, format_hex


class Generator():
    """Base generator class.

    :param rmap: Register map object
    :type rmap: :class:`regmapGen.RegisterMap`
    """

    def __init__(self, rmap, **args):
        self.rmap = rmap
        self.etc = args

    def _name(self):
        return self.__class__.__name__

    def generate(self):
        """Do file generation."""
        pass

    def validate(self):
        """Validate generator parameters."""
        # config
        config.validate_globcfg(config.globcfg)
        # rmap
        assert isinstance(self.rmap, RegisterMap), \
            "Register map has to be '%s', but '%s' was provided for '%s' generator!" % (
                repr(RegisterMap()), repr(self.rmap), self._name())
        self.rmap.validate()

    def make_target(self, name):
        """Dump class attributes to dictionary that can be used as target for `config` generation.

        :param name: Name of the target
        :return: Target dictionary
        """
        params = vars(self)
        params.pop('etc')
        params.pop('rmap')
        params['generator'] = self._name()
        return {name: params}


class Jinja2():
    """Basic class for rendering Jinja2 templates"""

    def get_jinja_env(self, templates_path):
        """Initialize Jinja2 environment.

        :param templates_path: Path to search templates
        :return: Jinja2 environment
        """
        j2_env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=templates_path),
                                    trim_blocks=True, lstrip_blocks=True)
        j2_env.globals.update(zip=zip)
        return j2_env

    def render(self, template, vars, templates_path=None):
        """Render text with Jinja2.

        :param template: Jinja2 template filename
        :param vars: Dictionary with variables for Jinja2 rendering
        :param templates_path: Path to search templates. If no path provided, then internal templates will be used
        :return: String with rendered text
        """
        # prepare template
        if not templates_path:
            templates_path = str(Path(__file__).parent / 'templates')
        j2_env = self.get_jinja_env(templates_path)
        j2_template = j2_env.get_template(template)
        # render
        return j2_template.render(vars)

    def render_to_file(self, template, vars, path, templates_path=None):
        """Render text with Jinja2 and save it to the file.

        :param template: Jinja2 template filename
        :param vars: Dictionary with variables for Jinja2 rendering
        :param path: Path to the output file
        :param templates_path: Path to search templates. If no path provided, then internal templates will be used
        """
        # render
        rendered_text = self.render(template, vars, templates_path)
        # save
        utils.create_dirs(path)
        with open(path, "w", encoding="utf-8") as f:
            f.write(rendered_text)


class Wavedrom():
    """Basic class for rendering register images with wavedrom"""

    def draw_regs(self, imgdir, rmap):
        imgdir.mkdir(exist_ok=True)

        bits = config.globcfg['data_width']
        lanes = bits // 8 if bits > 8 else 1
        for reg in rmap:
            reg_wd = {"reg": [],
                      "config": {"bits": bits, "lanes": lanes, "fontsize": 14, "vspace": 100, "fontfamily": 'Arial'}}
            bit_pos = -1
            for bf in reg:
                if bit_pos == -1 and bf.lsb > 0:
                    reg_wd["reg"].append({"bits": bf.lsb})
                elif bf.lsb - bit_pos > 1:
                    reg_wd["reg"].append({"bits": bf.lsb - bit_pos - 1})
                name = bf.name
                # name_max_len = 5 * bf.width
                # if len(bf.name) > name_max_len:  # to prevent labels overlapping
                #    name = bf.name[:name_max_len - 1] + '..'
                reg_wd["reg"].append({"name": name, "attr": bf.access, "bits": bf.width})
                bit_pos = bf.msb
            if (bits - 1) > bit_pos:
                reg_wd["reg"].append({"bits": bits - bit_pos - 1})
            wavedrom.render(json.dumps(reg_wd)).saveas(str(imgdir / ("%s.svg" % reg.name.lower())))


class Json(Generator):
    """Dump register map to a JSON file.

    :param rmap: Register map object
    :type rmap: :class:`regmapGen.RegisterMap`
    :param path: Path to the output file
    :type path: str
    """

    def __init__(self, rmap=None, path='regs.json', **args):
        super().__init__(rmap, **args)
        self.path = path

    def generate(self):
        # validate register map
        self.rmap.validate()
        # prepare data
        data = {'regmap': list(self.rmap.as_dict().values())}
        # dump
        utils.create_dirs(self.path)
        with open(self.path, 'w', encoding="utf-8") as f:
            json.dump(data, f, indent=4)


class Yaml(Generator):
    """Dump register map to a YAML file.

    :param rmap: Register map object
    :type rmap: :class:`regmapGen.RegisterMap`
    :param path: Path to the output file
    :type path: str
    """

    def __init__(self, rmap=None, path='regs.yaml', **args):
        super().__init__(rmap, **args)
        self.path = path

    def generate(self):
        # validate parameters
        self.validate()
        # prepare data
        data = {'regmap': list(self.rmap.as_dict().values())}
        # dump
        utils.create_dirs(self.path)
        with open(self.path, 'w', encoding="utf-8") as f:
            yaml.Dumper.ignore_aliases = lambda *args: True  # hack to disable aliases
            yaml.dump(data, f, indent=4, default_flow_style=False, sort_keys=False)


class Txt(Generator):
    """Dump register map to a text table.

    Note: only registers with single bitfield are allowed.

    :param rmap: Register map object
    :type rmap: :class:`regmapGen.RegisterMap`
    :param path: Path to the output file
    :type path: str
    """

    def __init__(self, rmap=None, path='regs.txt', **args):
        super().__init__(rmap, **args)
        self.path = path

    def generate(self):
        # validate parameters
        self.validate()
        for reg in self.rmap:
            if len(reg) > 1:
                raise ValueError("Only registers with single bitfield are allowed for %s generator." % self._name())
        # prepare template strings
        data_w = config.globcfg['data_width']
        address_w = config.globcfg['address_width']
        address_digits = address_w // 4 + (1 if address_w % 4 else 0)
        address_str = "0x%0{0}x".format(address_digits)
        reset_digits = data_w // 4 + (1 if data_w % 4 else 0)
        reset_str = "0x%0{0}x".format(reset_digits)
        row_template = "| %-{0}s | %-{1}s | %-{2}s | %-{3}s | %-{4}s | %-{5}s | %-{6}s |\n"
        # prepare table data
        row_top = ["Address", "Name", "Width", "Access", "Hardware", "Reset", "Description"]
        col_address = [address_str % reg.address for reg in self.rmap]
        col_names = self.rmap.reg_names
        col_width = ["%d" % reg.bitfields[0].width for reg in self.rmap]
        col_access = [reg.bitfields[0].access for reg in self.rmap]
        col_hardware = [reg.bitfields[0].hardware for reg in self.rmap]
        col_reset = [reset_str % reg.reset for reg in self.rmap]
        col_description = [reg.description for reg in self.rmap]
        # calculate width of the columns for pretty printing
        cols_w = [max(address_digits + 2, len(row_top[0])),
                  max(max([len(s) for s in col_names]), len(row_top[1])),
                  max(max([len(s) for s in col_width]), len(row_top[2])),
                  max(max([len(s) for s in col_access]), len(row_top[3])),
                  max(max([len(s) for s in col_hardware]), len(row_top[4])),
                  max(reset_digits + 2, len(row_top[5])),
                  max(max([len(s) for s in col_description]), len(row_top[6]))]
        row_template = row_template.format(*cols_w)
        # render
        out_lines = [row_template % tuple(row_top)]
        out_lines.append(row_template % tuple(["-" * w for w in cols_w]))
        for i in range(len(col_names)):
            out_lines.append(row_template % (col_address[i], col_names[i],
                             col_width[i], col_access[i], col_hardware[i], col_reset[i], col_description[i]))
        # save to file
        utils.create_dirs(self.path)
        with open(self.path, 'w', encoding="utf-8") as f:
            f.writelines(out_lines)


class Xls(Generator):
    """Copy register map to a Excel file from template.

    :param rmap: Register map object
    :type rmap: :class:`regmapGen.RegisterMap`
    :param path: Path to the output file
    :type path: str
    """

    def __init__(self, rmap=None, path='regs.xlsx', **args):
        super().__init__(rmap, **args)
        self.path = path

    def generate(self):
        # validate parameters
        self.validate()
        # copy excel data
        template_path = Path(__file__).parent / 'templates' / 'xls_example.xlsx'
        utils.create_dirs(self.path)
        shutil.copy(template_path, self.path)


class SystemVerilog(Generator, Jinja2):
    """Create SystemVerilog file with register map.

    :param rmap: Register map object
    :type rmap: :class:`regmapGen.RegisterMap`
    :param path: Path to the output file
    :type path: str
    :param read_filler: Numeric value to return if wrong address was read
    :type read_filler: int
    :param interface: Register map bus protocol. Use one of: `axil`, `apb`, `amm`, `spi`, `lb`
    :type interface: str
    :param template_path: A path to the template to use instead of the default template.
    :type template_path: str
    """

    def __init__(self, rmap=None, path='regs.sv', read_filler=0, interface='axil', template_path='', **args):
        super().__init__(rmap, **args)
        self.path = path
        self.read_filler = read_filler
        self.interface = interface
        self.template_path = template_path

    def validate(self):
        super().validate()
        assert self.interface in ['axil', 'apb', 'amm', 'spi', 'lb'], \
            "Unknown '%s' interface!" % (self.interface)

    def generate(self):
        # validate parameters
        self.validate()
        # prepare jinja2
        default_template = os.path.join(
            Path(__file__).parent, 'templates', 'regmap_sv.j2'
        )
        template_path = self.template_path if self.template_path != '' else default_template
        j2_template = Path(template_path).name
        j2_vars = {}
        j2_vars['regmapGen_ver'] = __version__
        j2_vars['rmap'] = self.rmap
        j2_vars['module_name'] = utils.get_file_name(self.path)
        j2_vars['read_filler'] = utils.str2int(self.read_filler)
        j2_vars['interface'] = self.interface
        j2_vars['config'] = config.globcfg
        # render
        self.render_to_file(j2_template, j2_vars, self.path, Path(template_path).parent)


class SystemVerilogWrapper(Generator, Jinja2):
    """Create SystemVerilog file with register map.

    :param rmap: Register map object
    :type rmap: :class:`regmapGen.RegisterMap`
    :param path: Path to the output file
    :type path: str
    :param module_name: Module name of register map
    :type module_name: str
    :param interface: Register map bus protocol. Use one of: `axil`, `apb`, `amm`, `spi`, `lb`
    :type interface: str
    :param template_path: A path to the template to use instead of the default template.
    :type template_path: str
    """

    def __init__(self, rmap=None, path='regs_wrapper.svh', module_name='regs', interface='axil',
                 template_path='', **args):
        super().__init__(rmap, **args)
        self.path = path
        self.module_name = module_name
        self.interface = interface
        self.template_path = template_path

    def validate(self):
        super().validate()
        assert self.interface in ['axil', 'apb', 'amm', 'spi', 'lb'], \
            "Unknown '%s' interface!" % (self.interface)

    def generate(self):
        # validate parameters
        self.validate()
        # prepare jinja2
        default_template = os.path.join(
            Path(__file__).parent, 'templates', 'sv_wrapper.j2'
        )
        template_path = self.template_path if self.template_path != '' else default_template
        j2_template = Path(template_path).name
        j2_vars = {}
        j2_vars['regmapGen_ver'] = __version__
        j2_vars['rmap'] = self.rmap
        j2_vars['module_name'] = self.module_name
        j2_vars['interface'] = self.interface
        j2_vars['config'] = config.globcfg
        # render
        self.render_to_file(j2_template, j2_vars, self.path, Path(template_path).parent)


class SystemVerilogHeader(Generator, Jinja2):
    """Create SystemVerilog header file with register map defines.

    :param rmap: Register map object
    :type rmap: :class:`regmapGen.RegisterMap`
    :param path: Path to the output file
    :type path: str
    :param prefix: Prefix for the all defines. Empty is allowed.
    :type prefix: str
    :param template_path: A path to the template to use instead of the default template.
    :type template_path: str
    """

    def __init__(self, rmap=None, path='regs.svh', prefix="", template_path='', **args):
        super().__init__(rmap, **args)
        self.path = path
        self.prefix = prefix
        self.template_path = template_path

    def generate(self):
        # validate parameters
        self.validate()
        # prepare jinja2
        default_template = os.path.join(
            Path(__file__).parent, 'templates', 'sv_header.j2'
        )
        template_path = self.template_path if self.template_path != '' else default_template
        j2_template = Path(template_path).name
        j2_vars = {}
        j2_vars['regmapGen_ver'] = __version__
        j2_vars['rmap'] = self.rmap
        j2_vars['prefix'] = self.prefix.upper()
        j2_vars['file_name'] = utils.get_file_name(self.path)
        j2_vars['config'] = config.globcfg
        # render
        self.render_to_file(j2_template, j2_vars, self.path, Path(template_path).parent)


class CHeader(Generator, Jinja2):
    """Create C header file with register map defines.

    :param rmap: Register map object
    :type rmap: :class:`regmapGen.RegisterMap`
    :param path: Path to the output file
    :type path: str
    :param prefix: Prefix for the all defines and types. Empty is allowed.
    :type prefix: str
    :param template_path: A path to the template to use instead of the default template.
    :type template_path: str
    """

    def __init__(self, rmap=None, path='regs.h', prefix="", template_path='', **args):
        super().__init__(rmap, **args)
        self.path = path
        self.prefix = prefix
        self.template_path = template_path

    def validate(self):
        super().validate()
        data_width_allowed = [8, 16, 32, 64]
        assert config.globcfg['data_width'] in [8, 16, 32, 64], \
            "For %s generator, global 'data_width' must be one of '%s', but current is %d" % \
            (self._name(), data_width_allowed, config.globcfg['data_width'])

    def generate(self):
        # validate parameters
        self.validate()
        # prepare jinja2
        default_template = os.path.join(
            Path(__file__).parent, 'templates', 'c_header.j2'
        )
        template_path = self.template_path if self.template_path != '' else default_template
        j2_template = Path(template_path).name
        j2_vars = {}
        j2_vars['regmapGen_ver'] = __version__
        j2_vars['rmap'] = self.rmap
        j2_vars['prefix'] = self.prefix.upper()
        j2_vars['file_name'] = utils.get_file_name(self.path)
        j2_vars['config'] = config.globcfg
        # render
        self.render_to_file(j2_template, j2_vars, self.path, Path(template_path).parent)


class SystemVerilogPackage(Generator, Jinja2):
    """Create SystemVerilog package with register map parameters.

    :param rmap: Register map object
    :type rmap: :class:`regmapGen.RegisterMap`
    :param path: Path to the output file
    :type path: str
    :param prefix: Prefix for the all parameters and types. Empty is allowed.
    :type prefix: str
    :param template_path: A path to the template to use instead of the default template.
    :type template_path: str
    """

    def __init__(self, rmap=None, path='regs_pkg.sv', prefix="", template_path='', **args):
        super().__init__(rmap, **args)
        self.path = path
        self.prefix = prefix
        self.template_path = template_path

    def generate(self):
        # validate parameters
        self.validate()
        # prepare jinja2
        default_template = os.path.join(
            Path(__file__).parent, 'templates', 'sv_package.j2'
        )
        template_path = self.template_path if self.template_path != '' else default_template
        j2_template = Path(template_path).name
        j2_vars = {}
        j2_vars['regmapGen_ver'] = __version__
        j2_vars['rmap'] = self.rmap
        j2_vars['prefix'] = self.prefix.upper()
        j2_vars['file_name'] = utils.get_file_name(self.path)
        j2_vars['config'] = config.globcfg
        # render
        self.render_to_file(j2_template, j2_vars, self.path, Path(template_path).parent)


class LbBridgeSystemVerilog(Generator, Jinja2):
    """Create SystemVerilog file with bridge to Local Bus.

    :param rmap: Register map object
    :type rmap: :class:`regmapGen.RegisterMap`
    :param path: Path to the output file
    :type path: str
    :param bridge_type: Bridge protocol. Use one of `axil`, `apb`, `amm`, `spi`.
    :type bridge_type: str
    :param template_path: A path to the template to use instead of the default template.
    :type template_path: str
    """

    def __init__(self, rmap=None, path='axil2lb.sv', bridge_type='axil', template_path='', **args):
        super().__init__(rmap, **args)
        self.path = path
        self.bridge_type = bridge_type
        self.template_path = template_path

    def validate(self):
        assert self.bridge_type in ['axil', 'apb', 'amm', 'spi'], \
            "Unknown '%s' bridge type!" % (self.bridge_type)

    def generate(self):
        # validate parameters
        self.validate()
        # prepare jinja2
        default_templates = {
            'axil': 'axil2lb_sv.j2',
            'apb': 'apb2lb_sv.j2',
            'amm': 'amm2lb_sv.j2',
            'spi': 'spi2lb_sv.j2'
        }
        default_template = os.path.join(
            Path(__file__).parent, 'templates', default_templates[self.bridge_type]
        )
        template_path = self.template_path if self.template_path != '' else default_template
        j2_template = Path(template_path).name
        j2_vars = {}
        j2_vars['regmapGen_ver'] = __version__
        j2_vars['module_name'] = utils.get_file_name(self.path)
        j2_vars['config'] = config.globcfg
        # render
        self.render_to_file(j2_template, j2_vars, self.path, Path(template_path).parent)


class Markdown(Generator, Jinja2, Wavedrom):
    """Create documentation for a register map in Markdown.

    :param rmap: Register map object
    :type rmap: :class:`regmapGen.RegisterMap`
    :param path: Path to the output file
    :type path: str
    :param title: Document title
    :type title: str
    :param print_images: Enable generating images for bit fields of a register
    :type print_images: bool
    :param image_dir: Path to directory where all images will be saved
    :type image_dir: str
    :param print_conventions: Enable generating table with register access modes explained
    :type print_conventions: bool
    :param template_path: A path to the template to use instead of the default template.
    :type template_path: str
    """

    def __init__(self, rmap=None, path='regs.md', title='Register map',
                 print_images=True, image_dir="regs_img", print_conventions=True, template_path='', **args):
        super().__init__(rmap, **args)
        self.path = path
        self.title = title
        self.print_images = print_images
        self.image_dir = image_dir
        self.print_conventions = print_conventions
        self.template_path = template_path

    def generate(self):
        filename = utils.get_file_name(self.path)
        # validate parameters
        self.validate()
        # prepare jinja2
        default_template = os.path.join(
            Path(__file__).parent, 'templates', 'regmap_md.j2'
        )
        template_path = self.template_path if self.template_path != '' else default_template
        j2_template = Path(template_path).name
        j2_vars = {}
        j2_vars['regmapGen_ver'] = __version__
        j2_vars['rmap'] = self.rmap
        j2_vars['print_images'] = utils.str2bool(self.print_images)
        j2_vars['print_conventions'] = utils.str2bool(self.print_conventions)
        j2_vars['image_dir'] = self.image_dir
        j2_vars['filename'] = filename
        j2_vars['title'] = self.title
        j2_vars['config'] = config.globcfg
        # render
        self.render_to_file(j2_template, j2_vars, self.path, Path(template_path).parent)
        # draw register images
        if self.print_images:
            self.draw_regs(Path(self.path).parent / self.image_dir, self.rmap)


class Asciidoc(Generator, Jinja2, Wavedrom):
    """Create documentation for a register map in AsciiDoc.

    :param rmap: Register map object
    :type rmap: :class:`regmapGen.RegisterMap`
    :param path: Path to the output file
    :type path: str
    :param title: Document title
    :type title: str
    :param print_images: Enable generating images for bit fields of a register
    :type print_images: bool
    :param image_dir: Path to directory where all images will be saved
    :type image_dir: str
    :param print_conventions: Enable generating table with register access modes explained
    :type print_conventions: bool
    :param template_path: A path to the template to use instead of the default template.
    :type template_path: str
    """

    def __init__(self, rmap=None, path='regs.adoc', title='Register map',
                 print_images=True, image_dir="regs_img", print_conventions=True, template_path='', **args):
        super().__init__(rmap, **args)
        self.path = path
        self.title = title
        self.print_images = print_images
        self.image_dir = image_dir
        self.print_conventions = print_conventions
        self.template_path = template_path

    def generate(self):
        filename = utils.get_file_name(self.path)
        # validate parameters
        self.validate()
        # prepare jinja2
        default_template = os.path.join(
            Path(__file__).parent, 'templates', 'regmap_asciidoc.j2'
        )
        template_path = self.template_path if self.template_path != '' else default_template
        j2_template = Path(template_path).name
        j2_vars = {}
        j2_vars['regmapGen_ver'] = __version__
        j2_vars['rmap'] = self.rmap
        j2_vars['print_images'] = utils.str2bool(self.print_images)
        j2_vars['print_conventions'] = utils.str2bool(self.print_conventions)
        j2_vars['image_dir'] = self.image_dir
        j2_vars['filename'] = filename
        j2_vars['title'] = self.title
        j2_vars['config'] = config.globcfg
        # render
        self.render_to_file(j2_template, j2_vars, self.path, Path(template_path).parent)
        # draw register images
        if self.print_images:
            self.draw_regs(Path(self.path).parent / self.image_dir, self.rmap)


class Rst(Generator, Jinja2, Wavedrom):
    """Create documentation for a register map in reStructuredText.
    :param rmap: Register map object
    :type rmap: :class:`regmapGen.RegisterMap`
    :param path: Path to the output file
    :type path: str
    :param title: Document title
    :type title: str
    :param print_images: Enable generating images for bit fields of a register
    :type print_images: bool
    :param image_dir: Path to directory where all images will be saved
    :type image_dir: str
    :param print_conventions: Enable generating table with register access modes explained
    :type print_conventions: bool
    :param template_path: A path to the template to use instead of the default template.
    :type template_path: str
    """

    def __init__(self, rmap=None, path='regs.rst', title='Register map',
                 print_images=True, image_dir="regs_img", print_conventions=True, template_path='', **args):
        super().__init__(rmap, **args)
        self.path = path
        self.title = title
        self.print_images = print_images
        self.image_dir = image_dir
        self.print_conventions = print_conventions
        self.template_path = template_path

    def generate(self):
        filename = utils.get_file_name(self.path)
        # validate parameters
        self.validate()
        # prepare jinja2
        default_template = os.path.join(
            Path(__file__).parent, 'templates', 'regmap_rst.j2'
        )
        template_path = self.template_path if self.template_path != '' else default_template
        j2_template = Path(template_path).name
        j2_vars = {}
        j2_vars['regmapGen_ver'] = __version__
        j2_vars['rmap'] = self.rmap
        j2_vars['print_images'] = utils.str2bool(self.print_images)
        j2_vars['print_conventions'] = utils.str2bool(self.print_conventions)
        j2_vars['image_dir'] = self.image_dir
        j2_vars['filename'] = filename
        j2_vars['title'] = self.title
        j2_vars['config'] = config.globcfg
        # render
        self.render_to_file(j2_template, j2_vars, self.path, Path(template_path).parent)
        # draw register images
        if self.print_images:
            self.draw_regs(Path(self.path).parent / self.image_dir, self.rmap)


class Docx(Generator):
    """Create documentation in Docx from Markdown using Pandoc.

    :param rmap: Register map object
    :type rmap: :class:`regmapGen.RegisterMap`
    :param input_md: Path to the input Markdown file
    :type input_md: str
    :param path: Path to the output DOCX file
    :type path: str
    :param pandoc_args: Additional arguments for Pandoc command-line tool
    :type pandoc_args: str or list
    """

    def __init__(self, rmap=None, path='regs.docx', input_md='regs.md', pandoc_args=None, **args):
        super().__init__(rmap, **args)
        self.path = path
        self.input_md = input_md
        self.pandoc_args = pandoc_args if pandoc_args else ''

    def generate(self):
        # Validate parameters
        self.validate()

        # Save current directory
        current_dir = os.getcwd()

        try:
            # Change directory to the specified path
            os.chdir(os.path.dirname(self.path))

            # Convert Markdown to Docx using Pandoc
            command = ['pandoc', '-s', '-o', os.path.basename(self.path), self.input_md]
            if self.pandoc_args:
                if isinstance(self.pandoc_args, str):
                    command.extend(self.pandoc_args.split())  # If pandoc_args is a string, split it by spaces
                else:
                    command.extend(self.pandoc_args)  # Otherwise, add the arguments as they are
            subprocess.run(command, check=True)
            print("... docx document generated successfully!")
        except subprocess.CalledProcessError as e:
            print(f"... docx document error generating: {e}")
        finally:
            # Change back to the original directory
            os.chdir(current_dir)


class CmsisSvd(Generator, Jinja2):
    """ Create the CMSIS SVD file.

    :param rmap: Register map object
    :type rmap: :class:`regmapGen.RegisterMap`
    :param path: Path to the output file
    :type path: str
    :param peripheral_name: Header SVD info - peripheral name
    :type peripheral_name: str
    :param description: Header SVD info - description
    :type description: str
    :param part_version: Header SVD info - version
    :type part_version: str
    :param template_path: A path to the template to use instead of the default template.
    :type template_path: str
    """

    def __init__(self, rmap=None, path='regs.svd', peripheral_name='CSR',
                 description='no description', part_version='1.0.0', template_path='', **args):
        super().__init__(rmap, **args)
        self.path = path
        self.peripheral_name = peripheral_name
        self.description = description
        self.part_version = part_version
        self.template_path = template_path

    def generate(self):
        # validate parameters
        self.validate()

        # prepare jinja2
        default_template = os.path.join(
            Path(__file__).parent, 'templates', 'cmsis_svd.j2'
        )
        template_path = self.template_path if self.template_path != '' else default_template
        j2_template = Path(template_path).name
        j2_vars = {}
        j2_vars['regmapGen_ver'] = __version__
        j2_vars['rmap'] = self.rmap
        j2_vars['peripheral_name'] = self.peripheral_name
        j2_vars['description'] = self.description
        j2_vars['part_version'] = self.part_version
        j2_vars['config'] = config.globcfg
        j2_vars['part_name'] = utils.get_file_name(self.path)
        # render
        self.render_to_file(j2_template, j2_vars, self.path, Path(template_path).parent)


class IpxactXml(Generator, Jinja2):
    """ Create the IP-XACT XML file.

    :param rmap: Register map object
    :type rmap: :class:`regmapGen.RegisterMap`
    :param path: Path to the output file
    :type path: str
    :param vendor: Header XML info - Vendor
    :type vendor: str
    :param library: Header XML info - library
    :type library: str
    :param component_name: Header XML info - component name
    :type component_name: str
    :param version: Header XML info - version
    :type version: str
    :param memorymap_name: Header XML info - memorymap name
    :type memorymap_name: str
    :param addressblock_name: Header XML info - addressblock name
    :type addressblock_name: str
    :param description: Header XML info - description
    :type description: str
    :param template_path: A path to the template to use instead of the default template.
    :type template_path: str
    """

    def __init__(self, rmap=None, path='regs.xml', vendor='NM-Tech',
                 library='No library', component_name='No component_name', version='No version',
                 memorymap_name='No memorymap_name', addressblock_name='No addressblock_name',
                 description='No description', template_path='', **args):
        super().__init__(rmap, **args)
        self.path = path
        self.vendor = vendor
        self.library = library
        self.component_name = component_name
        self.version = version
        self.memorymap_name = memorymap_name
        self.addressblock_name = addressblock_name
        self.description = description
        self.template_path = template_path

    def generate(self):
        # validate parameters
        self.validate()

        # prepare jinja2
        default_template = os.path.join(
            Path(__file__).parent, 'templates', 'ipxact_xml.j2'
        )
        template_path = self.template_path if self.template_path != '' else default_template
        j2_template = Path(template_path).name
        j2_vars = {}
        j2_vars['regmapGen_ver'] = __version__
        j2_vars['rmap'] = self.rmap
        j2_vars['vendor'] = self.vendor
        j2_vars['library'] = self.library
        j2_vars['component_name'] = self.component_name
        j2_vars['version'] = self.version
        j2_vars['memorymap_name'] = self.memorymap_name
        j2_vars['addressblock_name'] = self.addressblock_name
        j2_vars['description'] = self.description
        j2_vars['config'] = config.globcfg
        j2_vars['part_name'] = utils.get_file_name(self.path)

        # render
        self.render_to_file(j2_template, j2_vars, self.path, Path(template_path).parent)


class Python(Generator, Jinja2):
    """Create Python file to access register map via some interface.

    :param rmap: Register map object
    :type rmap: :class:`regmapGen.RegisterMap`
    :param path: Path to the output file
    :type path: str
    :param template_path: A path to the template to use instead of the default template.
    :type template_path: str
    """

    def __init__(self, rmap=None, path='regs.py', template_path='', **args):
        super().__init__(rmap, **args)
        self.path = path
        self.template_path = template_path

    def generate(self):
        # validate parameters
        self.validate()
        # prepare jinja2
        default_template = os.path.join(
            Path(__file__).parent, 'templates', 'regmap_py.j2'
        )
        template_path = self.template_path if self.template_path != '' else default_template
        j2_template = Path(template_path).name
        j2_vars = {}
        j2_vars['regmapGen_ver'] = __version__
        j2_vars['rmap'] = self.rmap
        j2_vars['config'] = config.globcfg
        # render
        self.render_to_file(j2_template, j2_vars, self.path, Path(template_path).parent)


class Xls2Uvm(Generator, Jinja2):
    """Create UVM register model from Excel file with register map.

    :param rmap: Register map object (not used here but kept for consistency)
    :type rmap: :class:`regmapGen.RegisterMap`
    :param path: Path to the output file
    :type path: str
    :param input_xls: Path to the input Excel file
    :type input_xls: str
    :param template_path: Path to the Jinja2 template file
    :type template_path: str
    :param module_name: Name of the module
    :type module_name: str
    :param use_factory: Flag to use UVM factory
    :type use_factory: bool
    :param use_coverage: Flag to use functional coverage
    :type use_coverage: bool
    """

    def __init__(self, rmap=None, path='uvm_regmodel.sv', input_xls='regs.xlsx', template_path='',
                 module_name='uvm', use_factory='', use_coverage='', **args):
        super().__init__(rmap, **args)
        self.path = path
        self.input_xls = input_xls
        self.template_path = template_path
        self.module_name = module_name
        self.use_factory = use_factory
        self.use_coverage = use_coverage

    def get_jinja_env(self, templates_path):
        j2_env = super().get_jinja_env(templates_path)
        # j2_env.filters['get_bit_reset'] = get_bit_reset
        j2_env.filters['format_hex'] = format_hex
        return j2_env

    def generate(self):
        parser = XLSParser()
        parser.get_sheet(self.input_xls)
        # prepare jinja2
        default_template = os.path.join(
            Path(__file__).parent, 'templates', 'uvm_regmodel.j2'
        )
        template_path = self.template_path if self.template_path != '' else default_template
        template_name = Path(template_path).name
        j2_vars = {}
        j2_vars['rmap'] = parser.parse_data()
        j2_vars['regmapGen_ver'] = __version__
        j2_vars['path'] = Path(self.path).name
        j2_vars['module'] = self.module_name
        j2_vars['width'] = config.globcfg['data_width']
        j2_vars['factory'] = self.use_factory
        j2_vars['coverage'] = "UVM_CVR_ALL" if self.use_coverage else "UVM_NO_COVERAGE"
        # render
        self.render_to_file(template_name, j2_vars, self.path, Path(template_path).parent)


class Xls2Html(Generator, Jinja2):
    """Create HTML documentation from Excel file with register map.

    :param rmap: Register map object (not used here but kept for consistency)
    :type rmap: :class:`regmapGen.RegisterMap`
    :param path: Path to the output directory
    :type path: str
    :param title: Document title
    :type title: str
    :param input_xls: Path to the input Excel file
    :type input_xls: str
    :param template_path: Path to the Jinja2 template file
    :type template_path: str
    """

    def __init__(self, rmap=None, path='regs.html', title='Register map',
                 input_xls='regs.xlsx', template_path='', **args):
        super().__init__(rmap, **args)
        self.path = path
        self.title = title
        self.input_xls = input_xls
        self.template_path = template_path

    def get_jinja_env(self, templates_path):
        j2_env = super().get_jinja_env(templates_path)
        j2_env.filters['get_bit_reset'] = get_bit_reset
        j2_env.filters['format_hex'] = format_hex
        return j2_env

    def generate(self):
        parser = XLSParser()
        parser.get_sheet(self.input_xls)
        rmap = parser.parse_data()
        # prepare jinja2
        default_template = os.path.join(
            Path(__file__).parent, 'templates', 'html.j2'
        )
        template_path = self.template_path if self.template_path != '' else default_template
        template_name = Path(template_path).name
        j2_vars = {}
        j2_vars['rmap'] = rmap
        j2_vars['rmap'] = parser.fill_reserved(rmap)
        j2_vars['rmap'] = parser.reorder_by_lsb(j2_vars['rmap'])
        j2_vars['title'] = self.title
        # prepare html source
        output_dir = os.path.dirname(self.path)
        src = os.path.join(Path(__file__).parent, 'html')
        des = os.path.join(output_dir, 'html_src')
        if os.path.isdir(des):
            shutil.rmtree(des)
        shutil.copytree(src, des)
        # render
        self.render_to_file(template_name, j2_vars, self.path, Path(template_path).parent)
