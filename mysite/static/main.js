$( document ).ready(function() {

  var data = {"art": null, "politics": null, "author": null, "actor": null, "crime": null, "philanthropy": null, "music": null, "health": null, "gaming": null, "government": null, "business": null, "director": null, "adult": null, "unique": null, "tourism": null, "restaurant": null, "science": null, "medical": null, "academic": null, "tech": null, "journalist": null, "military": null, "nonprofit": null, "retail": null, "athlete": null, "food": null}

  $('#desc').autocomplete({
    data: data,
    limit: 6, // The max amount of results that can be shown at once. Default: Infinity.
    onAutocomplete: function (val) {
      // Callback function when value is autcompleted.
    },
    minLength: 1, // The minimum length of the input for the autocomplete to start. Default: 1.
  })

  $('input[type=radio]').on('change', function() {
    $(this).closest("form").submit();
  })

  $('#desc, #topic').on('keydown', function(event) {
    $('.filter-input').attr('checked', false)
    $('.filter').hide()

    if (event.keyCode == 13) {
      $(this).closest('form').submit()
      return false
    } else if (this.id == 'desc' && event.keyCode == 32) {
      return false
    }

  })

})
