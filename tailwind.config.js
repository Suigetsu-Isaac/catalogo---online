/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/*.html","./templates/img/{*.jpg,*.png}","./templates/static/js/*js"],
  theme: {
    extend: {
    
      textColor:[
      {primaryTextColor: "#ffffff"},
      {secoundTextColor: "#312e2d"},
      {titleTextColor: "#000000"},
      {inversionTextColor: "#fcc404"},
      {inversionMenu:"#ffa500"}
      ],
      backgroundColor:[
        {secoundBackground: "#f4f4f4"},
        {darkBackground: "#212932"},
        {primaryBackground: "#fcc404"},
        {backgroundMenu: "#ffa500"},
      ],
    },
  },
  plugins: [],
}

