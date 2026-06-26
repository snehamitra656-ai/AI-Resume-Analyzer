const fileInput =
document.getElementById("file");


const filename =
document.getElementById("filename");



fileInput.addEventListener(
"change",
()=>{


if(fileInput.files.length){


filename.innerHTML =
"✅ " + fileInput.files[0].name;


}


});




function scrollUpload(){


document
.getElementById("upload")
.scrollIntoView({

behavior:"smooth"

});


}





const form =
document.querySelector("form");


const btn =
document.querySelector(".analyze-btn");



form.addEventListener(
"submit",
()=>{


btn.innerHTML =
"🤖 AI Analyzing...";


btn.disabled=true;


});