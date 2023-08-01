let openNavBtn = document.getElementById("openNav");
let sidebar = document.getElementById("sidebar");
let closeNavBtn = document.getElementById("closeNav");

openNavBtn.onclick = () =>{
    sidebar.style.transform = "translateX(0)";
}
closeNavBtn.onclick = () =>{
    sidebar.style.transform = "translateX(-100%)";
}