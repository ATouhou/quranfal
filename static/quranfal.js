/**
 * Created by mehmet on 6/26/2016.
 */


function convert_aya_to_words(aya, display_word_meanings, learning, words_to_highlight) {
    var meanings = word_meanings[aya.id]
    var sura_number = aya.attributes['data-sura'].value
    var aya_number = aya.attributes['data-aya'].value
    var old_html = aya.innerHTML
    var new_html = ''
    var words = old_html.trim().split(' ')

    words_to_highlight = words_to_highlight.map(function (word) {
        return remove_diacritics(word)
    })

    words.forEach(function (word, index) {

        // highlight words if necessary
        words_to_highlight.forEach(function (word_to_highlight) {
            if (remove_diacritics(word).indexOf(word_to_highlight) >= 0) { // word_to_highlight might be a substring of the word
                word = '<span class="highlighted_word">' + word + '</span>'
                // todo break loop here - if word highlighted once
            }
        })

        if (display_word_meanings && !learning)
            new_html += '<div class="word_wrapper" data-word="' + index + '">'
                + '<div class="word">'
                + '<a class="word" href="{{base_url}}' + sura_number + '/' + aya_number + '/' + (index + 1) + '/" target="_blank">' + word + '</a>'
                + '</div><br><div class="word_meaning ltr_safe">&nbsp;' + meanings[index] + '&nbsp;|</div></div>'
        else if (learning)
            new_html += '<div class="word_wrapper" data-word="' + (index + 1) + '">'
                + '<div class="study button"></div>'
                + '<div class="word">' + word + '</div>'
                + '<div class="details" title="&lrm;' + meanings[index] + '&lrm;"></div>'
                + '<div class="known button"></div>'
                + '</div>'
        else
            new_html += '<div class="word_wrapper" data-word="' + index + '">'
                + '<div class="word">'
                + '<a class="word" href="{{base_url}}' + sura_number + '/' + aya_number + '/' + (index + 1) + '/" title="&lrm;' + meanings[index] + '&lrm;" target="_blank">' + word + '</a>'
                + '</div></div>'
    })

    aya.innerHTML = new_html
}


// CSRF code
function getCookie(name) {
    var cookieValue = null
    var i = 0
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';')
        for (i; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i])
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
                break
            }
        }
    }
    return cookieValue
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method))
}

