<li> 
    <blockquote class="${status_css} ${time_css}">
        <span class="icon status ${status_css}" role="presentation">
            <but    ton class='btn icon only'>
                ${api.icon('plus')}
            </button>
        </span>
        <div>
        <h5>${title}</h5>
        <div class='layout flex'>
            <p>
                ${description}
            </p>
            <div class="btn-container">
            ${request.layout_manager.render_panel(button.panel_name, context=button)}
            </div>
            </div>
        </div>
    </blockquote>
</li>