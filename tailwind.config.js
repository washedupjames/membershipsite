/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./membersite/membersite/templates/pages/home.html",
    "./membersite/membersite/templates/navbar.html",
    "./membersite/membersite/templates/base.html",
    "./membersite/membersite/templates/content/course_list.html",
    "./membersite/membersite/templates/content/course_detail.html",
    "./membersite/membersite/templates/payment/enroll.html",

    "./node_modules/flowbite/**/*.js",
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('flowbite/plugin')
  ],
}
