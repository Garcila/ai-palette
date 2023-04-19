const form = document.getElementById("create-form");
const container = document.querySelector(".container");

form.addEventListener("submit", function (e) {
	e.preventDefault();
	get_colors();
});

function get_colors() {
	const query = form.elements.query.value;
	fetch("/palette", {
		method: "POST",
		headers: {
			"Content-Type": "application/x-www-form-urlencoded",
		},
		body: new URLSearchParams({
			query: query,
		}),
	})
		.then(response => response.json())
		.then(data => {
			const colors = data.colors;
			create_color_html(colors, container);
		});
}

function create_color_html(colors, parent) {
	parent.innerHTML = "";
	for (const color of colors) {
		const div = document.createElement("div");
		div.classList.add("color");
		div.style.backgroundColor = color;
		// div.style.width = `calc(100% / ${colors.length})`; option if not using Flexbox

		div.addEventListener("click", function () {
			navigator.clipboard.writeText(color);
		});

		const span = document.createElement("span");
		span.innerText = color;
		div.appendChild(span);
		parent.appendChild(div);
	}
}
