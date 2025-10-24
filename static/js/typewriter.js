function typeWriterWords(text, element, speed = 150) {
    if (!element || !text) return;
    element.value = '';
    const words = text.split(' ');
    let i = 0;

    function writeWord() {
        if (i < words.length) {
            element.value += (i === 0 ? '' : ' ') + words[i];
            i++;
            setTimeout(writeWord, speed);
        }
    }

    writeWord();
}
