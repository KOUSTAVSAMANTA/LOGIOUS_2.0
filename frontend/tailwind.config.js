/** @type {import('tailwindcss').Config} */
export default {
	content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
	theme: {
		extend: {
			boxShadow: {
				right: '4px 0 10px 0 rgba(0, 0, 0, 0.1)' // Adjust the values as needed
			  }
		},
	},
	// eslint-disable-next-line no-undef
	plugins: [require("daisyui")],
};
