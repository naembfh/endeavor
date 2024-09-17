/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

const { Container } = require('postcss');

module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'
    ],
    theme: {
        screen:{
            sm: "340px",
            md: "540px",
            lg: "768px",
            xl: "1180px"
        },
        fontFamily: {
            Jost: ["Jost", "sans-serif"],
            Lobster: ["Lobster", "sans-serif"]
        },
        extend: {},
        keyframes: {
            move: {
                "50%": { transform: "translateY(-1rem)" }
            },
            rotate: {
                "0%": { transform: "rotate(0deg)" },
                "100%": { transform: "rotate(360deg)" }
            },
            scaleUp: {
                "0%": { transform: "scale(0.8)" },  // Removed "deg" from scale
                "50%": { transform: "scale(1.2)" },
                "100%": { transform: "scale(0.8)" }
            }
        },
        animation: {
            movingY: "move 3s linear infinite",      // Fixed typo: "infinate" to "infinite"
            rotating: "rotate 15s linear infinite",  // Fixed typo
            scalingUp: "scaleUp 15s linear infinite" // Fixed typo
        },
        
        container: {
            center: true,
            padding : {
                DEFAULT : "12px",
                md: "32px",
            }
        }
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
