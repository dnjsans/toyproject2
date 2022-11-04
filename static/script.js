const list = document.getElementById('list');

function showList(val = '') {
    $.ajax({
        type: "get",
        url: "/music",
        data: {},
        success: function (response) {
            let rows = response
            list.innerHTML = '';
            const res = rows.forEach(music => {
                    if (music.artist.includes(val)) {
                        const li = document.createElement('li');
                        li.innerHTML = `
                                            가수 : ${music.artist} <br> 제목 : ${music.title}
                                            `
                        list.appendChild(li);
                    }
                }
            )
        }
    })
}

showList();

const searchInput = document.getElementById('search');
const searchBtn = document.getElementById('searchBtn');

searchBtn.addEventListener('click', (e) => {
    e.preventDefault();
    const val = searchInput.value;
    console.log(val);
    showList(val);
})
