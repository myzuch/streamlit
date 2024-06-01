const sentences = document.querySelectorAll('.sentence');

sentences.forEach(sentence => {
  let originalInnerHTML
  const chunkId = sentence.getAttribute('ref');
  const sentenceText = sentence.textContent;
  const highlightElement = document.getElementById(chunkId);

  sentence.addEventListener('mouseover', () => {
    originalInnerHTML = highlightElement.innerHTML;
    highlight(highlightElement, sentenceText);
  });
  sentence.addEventListener('mouseout', () => {
    highlightElement.innerHTML = originalInnerHTML;
  });
  sentence.addEventListener('click', () => {
    scrollToChunk(chunkId);
  });
});

function highlight(highlightElement, text) {
  var innerHTML = highlightElement.innerHTML
  var index = innerHTML.toLowerCase().indexOf(text.toLowerCase());
  if (index >= 0) { 
   innerHTML = innerHTML.substring(0,index) + "<span class='highlight'>" + innerHTML.substring(index,index+text.length) + "</span>" + innerHTML.substring(index + text.length);
   highlightElement.innerHTML = innerHTML;
  }
  if (index == -1){
    innerHTML = "<span class='highlight'>" + innerHTML + "</span>";
    highlightElement.innerHTML = innerHTML;
  }
}

function scrollToChunk(chunkId) {
  const chunkToScroll = document.getElementById(chunkId);

  if (chunkToScroll) {
    chunkToScroll.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'nearest' });
  }
}
