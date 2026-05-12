function toggle(el, videoId) {
    const answer = el.nextElementSibling;
    const icon = el.querySelector('.faq-icon');
    const isOpen = answer.style.display !== 'none';

    document.querySelectorAll('.faq-answer').forEach(a => a.style.display = 'none');
    document.querySelectorAll('.faq-question .faq-icon').forEach(i => i.textContent = '+');
    document.querySelectorAll('.video-panel').forEach(v => {
        v.style.display = 'none';
        v.querySelector('video').pause();
    });

    if (!isOpen) {
        answer.style.display = 'block';
        icon.textContent = '-';
        document.getElementById(videoId).style.display = 'block';
    }
}