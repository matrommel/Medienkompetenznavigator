jQuery(function($) {
    function initAccordions() {
        $(".accordion").accordion({
            collapsible: true,
            active: false,
            heightStyle: "content"
        });
    }

    function loadJSON(callback) {
        $.getJSON(medienkompetenznavigator_vars.json_url)
            .done(function(data) {
                callback(data);
            })
            .fail(function(jqxhr, textStatus, error) {
                console.error("Request Failed: " + textStatus + ", " + error);
            });
    }

    function formatLernziele(lernziele) {
        return lernziele.map(ziel => ziel.replace(/\*/g, '<br>*')).join('<br>');
    }

    function formatKompetenzen(kompetenzen) {
        return kompetenzen.join(',<br>');
    }

    function createAccordion(data) {
        if (!data) {
            console.error("Invalid JSON data structure");
            return;
        }

        let accordionHtml = '';

        // Gruppiere Daten nach Beruf
        let berufGruppen = {};
        data.forEach(berufObj => {
            if (!berufGruppen[berufObj.Beruf]) {
                berufGruppen[berufObj.Beruf] = [];
            }
            berufGruppen[berufObj.Beruf].push(berufObj);
        });

        Object.keys(berufGruppen).forEach(beruf => {
            accordionHtml += `<h3 class="beruf">${beruf}</h3><div>`;

            berufGruppen[beruf].forEach(berufObj => {
                berufObj.Jahrgang.forEach(jahrgangObj => {
                    accordionHtml += `<h4 class="jahrgang">${jahrgangObj.Abschnitt}</h4><div>`;
                    jahrgangObj.Fächer.forEach(fach => {
                        accordionHtml += `<div class="accordion"><h3>${fach.Bezeichnung}</h3><div>`;
                        fach.lernsituation.forEach(lernsituation => {
                            accordionHtml += `<div class="accordion"><h3>${lernsituation.thema}</h3><div>`;
                            accordionHtml += `<p><strong>Lernziele:</strong> ${formatLernziele(lernsituation.lernziele)}</p>`;
                            accordionHtml += `<p><strong>Vorschlagslink:</strong> <a href="${lernsituation.vorschlagslink}">Link</a></p>`;
                            if (lernsituation.lerninhalt) {
                                accordionHtml += `<p><strong>Lerninhalt:</strong> ${lernsituation.lerninhalt.join(', ')}</p>`;
                            }
                    s
                            if (lernsituation.kompetenzen) {
                                accordionHtml += `<p><strong>Kompetenzen:</strong> ${formatKompetenzen(lernsituation.kompetenzen)}</p>`;
                            }
                            accordionHtml += `</div></div>`;
                        });
                        accordionHtml += `</div></div>`;
                    });
                    accordionHtml += `</div>`;
                });
            });

            accordionHtml += `</div>`;
        });

        $('#accordion').html(accordionHtml);
        initAccordions();
    }

    loadJSON(createAccordion);
});