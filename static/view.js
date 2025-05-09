$(document).ready(function() {
    $('.clickable-icon').on('click', function() {
        const $icon = $(this);
        const contentType = $icon.data('content-type');
        const content = $icon.data('content');
        
        $('#display-title').hide();
        
        if (contentType === "Core Idea" || contentType === "Why It's Effective" || contentType === "How to Spot It") {
            $('#display-content').html(`
                <p><strong>${contentType}:</strong> ${content}</p>
            `);
        } 
        else if (contentType === "Example") {
            if (isYouTubeUrl(content)) {
                $('#display-content').html(`
                    <div class="responsive-video-container mt-3">
                        <iframe src="${convertToEmbedUrl(content)}" 
                                frameborder="0" 
                                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                                allowfullscreen></iframe>
                    </div>
                `);
            } else {
                $('#display-content').html(`
                    <p><strong>${contentType}:</strong> 
                        <a href="${content}" target="_blank">View Example</a>
                    </p>
                `);
            }
        }
    });

    function isYouTubeUrl(url) {
        return url.includes('youtube.com') || url.includes('youtu.be');
    }

    function convertToEmbedUrl(url) {
        // Convert YouTube watch URL to embed URL
        if (url.includes('youtube.com/watch')) {
            const videoId = url.split('v=')[1].split('&')[0];
            return `https://www.youtube.com/embed/${videoId}`;
        }
        if (url.includes('youtu.be')) {
            const videoId = url.split('youtu.be/')[1].split('?')[0];
            return `https://www.youtube.com/embed/${videoId}`;
        }
        return url;
    }
});
