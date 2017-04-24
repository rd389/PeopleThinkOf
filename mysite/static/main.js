$( document ).ready(function() {

  $('#input').autocomplete({
    data: {
      "fun": null,
      "rich": null,
      "stupid": null,
      "fancy": null,
      "weird": null,
      "sassy": null,
      "sloppy": null,
      "salty": null,
      "petty": null,
      "pretty": null,
      "sad": null
    },
    limit: 6, // The max amount of results that can be shown at once. Default: Infinity.
    onAutocomplete: function (val) {
      // Callback function when value is autcompleted.
    },
    minLength: 1, // The minimum length of the input for the autocomplete to start. Default: 1.
  })

})
