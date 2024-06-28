jQuery(document).ready(function($){
	var $sub_menu = $('.regmapGen-reg-block'),
		$dummy_anchor = $(".section");

	$sub_menu.children('a').on('click', function(event) {
		event.preventDefault();
		$(this).toggleClass('block-open').next('ul').slideToggle(200).end().parent('.regmapGen-reg-block').siblings('.regmapGen-reg-block').children('a').removeClass('block-open').next('ul').slideUp(200);
	});

	$dummy_anchor.addClass("regmapGen-dummy-anchor");
});
