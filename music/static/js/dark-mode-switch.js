!function () {
    var t, e = document.getElementById("darkSwitch");
    if (e) {
        t = null !== localStorage.getItem("darkSwitch") && "dark" === localStorage.getItem("darkSwitch"), (e.checked = t) ? document.body.setAttribute("data-theme", "dark") : document.body.removeAttribute("data-theme"), e.addEventListener("change", function (t) {
            e.checked ? (document.body.setAttribute("data-theme", "dark"), localStorage.setItem("darkSwitch", "dark")) : (document.body.removeAttribute("data-theme"), localStorage.removeItem("darkSwitch"))
        })
    }
}();