// tailwind.config.js
module.exports = {
  content: ["./movies/templates/**/*.html", "./movies/static/**/*.css"],
  theme: {
    extend: {
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
};

