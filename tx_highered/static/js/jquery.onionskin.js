/* jQuery onionskin plugin */

$.fn.onionize = function(options){
    function fold($el, activateEvents){
      if (activateEvents !== false && options.beforeFold){
        options.beforeFold.call(this, "TODO", {elem: $el});
      }
      var data = $el.data('onion');
      data.$items.each(function(idx){
        var $this = $(this);
        if (options.animate){
          $this.animate({
            left: data.targetLeft,
            opacity: 1 / data.$items.length
          }, "slow");
        } else {
          $this.css({
            left: data.targetLeft,
            opacity: 1 / data.$items.length});
        }
      });
      $el.addClass('ui-onion-active');
      if (activateEvents !== false && options.afterFold){
        options.afterFold.call(this, "TODO", {elem: $el});
      }
    }

    function unfold($el, activateEvents){
      if (activateEvents !== false && options.beforeUnfold){
        options.beforeUnfold.call(this, "TODO", {elem: $el});
      }
      var data = $el.data('onion');
      data.$items.each(function(idx){
        var $this = $(this);
        var left = data.lefts[idx];
        if (options.animate){
          $this.animate({
            left: left,
            opacity: 1
          }, "slow");
        } else {
          $this.css({
            left: left,
            opacity: 1});
        }
      });
      $el.removeClass('ui-onion-active');
      if (activateEvents !== false && options.afterUnfold){
        options.afterUnfold.call(this, "TODO", {elem: $el});
      }
    }
    // catch API calls, TODO this is hacked on
    if (typeof options === "string") {
      switch (options){
        case 'fold':
          this.each(function(){
            fold($(this), false);
          });
        break;
        case 'unfold':
          this.each(function(){
            unfold($(this), false);
          });
        break;
      }

      return this;
    }
    options = options || {animate: true};

    this.each(function(){
      // setup
      var $el = $(this);
      var $button = $el.find(".onion-toggle");
      var $items = $el.find('.onion-item');
      var $onionBasket = $el.find('.onion-basket');
      var $centerItem = $items.eq($items.length>>1);
      var $legend = $el.find(".onion-legend");
      var $legendItems = $legend.find('.onion-legend-item');

      // calculate positions
      $onionBasket.css('position', 'relative');  // force basket to be offset parent
      var lefts = [];
      var targetLeft;
      $items.each(function(idx){
        var $this = $(this);
        var left = $this.position().left;
        lefts[idx] = left;
      });
      targetLeft = lefts[$items.length>>1];

      // save data
      var data = {};
      data.$items = $items;
      data.lefts = lefts;
      data.targetLeft = targetLeft;
      $el.data('onion', data);

      // convert to absolute positioning
      $onionBasket.css({
        height: $onionBasket.height(),
        width: "100%"
      });
      $items.each(function(idx){
        var $this = $(this);
        $this.css({
          'position': 'absolute',
          'left': data.lefts[idx]
        });
      });

      $button.click(function(){
        if ($el.hasClass('ui-onion-active')) {
          unfold($el);
        } else {
          fold($el);
        }
      });

      var featured;
      $legendItems.each(function(idx){
        var $this = $(this);
        $this.hover(function(){
          $this.addClass('active');
          featured = $items.eq(idx).clone(true);
          featured.addClass('ui-onion-item-active').css('opacity', 1).appendTo($onionBasket);
        }, function(){
          $this.removeClass('active');
          featured.remove();
        });
      });
    });
  };
