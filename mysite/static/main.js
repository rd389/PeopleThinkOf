$( document ).ready(function() {

  var data = {"art": null, "nsfw": null, "politics": null, "author": null, "travel": null, "actor": null, "crime": null, "philanthropy": null, "music": null, "health": null, "gaming": null, "municipal": null, "business": null, "director": null, "adult": null, "unique": null, "tourism": null, "customerservice": null, "restaurant": null, "science": null, "medical": null, "request": null, "academic": null, "tech": null, "journalist": null, "military": null, "nonprofit": null, "retail": null, "specialized": null, "athlete": null}

  $('#desc').autocomplete({
    data: data,
    limit: 6, // The max amount of results that can be shown at once. Default: Infinity.
    onAutocomplete: function (val) {
      // Callback function when value is autcompleted.
    },
    minLength: 1, // The minimum length of the input for the autocomplete to start. Default: 1.
  })

})
