const path = require('path');

const glob = require('glob-all');

const PurgecssPlugin = require('purgecss-webpack-plugin');

const OptimizeCssAssetsPlugin = require('optimize-css-assets-webpack-plugin');

const layouts = require('handlebars-layouts');

//reload browsers on every change

const BrowserSyncPlugin = require('browser-sync-webpack-plugin');

//extract css from javascript modules
const ExtractTextPlugin = require('extract-text-webpack-plugin');

//show some notifications

const WebpackNotifier = require('webpack-notifier');

//use handlebars as template engine for building UI
const HandlebarsPlugin = require('handlebars-webpack-plugin');

const pretty = require('pretty');

const mode = process.env.NODE_ENV || 'development';

const inProduction = mode === 'production';

//copy assets from the src directory to the dist directory
const CopyWebpackPlugin = require('copy-webpack-plugin');

const CleanWebpackPlugin = require('clean-webpack-plugin');

const ImageminPlugin = require('imagemin-webpack-plugin').default;

const config = {
    mode,
    //entry points
    entry: {
        css: './src/sass/app.scss',
        js: './src/js/app.js'
    },

    //destination for trans-piled files
    output: {
        path: path.resolve(__dirname, 'dist'),
        filename: '[name]/app.[name]'
    },
    performance: {
        hints: false
    },
    stats: {
        entrypoints: false
    },
    module: {
        rules: [
            {
                test: path.resolve(__dirname, 'src/js/app.js'),
                loader: 'babel-loader'
            },
            {
                //use absolute path to speed up module resolution instead of regular expressions like test:/\.scss$/
                test: path.resolve(__dirname, 'src/sass/app.scss'),
                use: ExtractTextPlugin.extract({
                    fallback: 'style-loader',
                    use: [
                        {
                            loader: 'css-loader'
                        },
                        {
                            loader: 'postcss-loader',
                            options: {
                                ident: 'postcss',
                                plugins: [
                                    new require('autoprefixer')({
                                        browsers: ['>1%'],
                                        // dont add old flexbox spec properties for webkit
                                        flexbox: 'no-2009'
                                    }),
                                    require('css-mqpacker')({ sort: true })
                                ]
                            }
                        },

                        {
                            loader: 'sass-loader',
                            options: {
                                //use 8 decimal places for all sass calculations
                                precision: 8
                            }
                        }
                    ]
                })
            }
        ]
    },

    plugins: [
        new CleanWebpackPlugin([path.resolve(__dirname, 'dist')]),
        new WebpackNotifier({
            alwaysNotify: true,
            title: 'Compilation was successful',
            contentImage: path.resolve(__dirname, 'andela.png')
        }),
        new CopyWebpackPlugin([
            {
                from: path.resolve(__dirname, 'src/images'),
                to: path.resolve(__dirname, 'dist/images')
            }
        ]),
        new ImageminPlugin({
            test: /\.(jpe?g|png|gif|svg)$/i,
            disable: mode === 'development'
        }),

        new HandlebarsPlugin({
            entry: path.join(__dirname, 'src', 'pages', '*.hbs'),
            output: path.join(__dirname, 'dist', '[name].html'),
            partials: [path.join(__dirname, 'src', '**', '*.hbs')],
            data: path.join(__dirname, 'src/dummyData.json'),

            onBeforeSave(Handlebars, resultHtml) {
                //prettify html
                return pretty(resultHtml);
            },
            onBeforeSetup(handlebars) {
                handlebars.registerHelper(layouts(handlebars));
            }
        }),
        //extract css out of the js modules
        new ExtractTextPlugin('css/app.css')
    ]
};

if (!inProduction) {
    // add browserSync only in development
    config.plugins.push(
        new BrowserSyncPlugin({
            port: 7000,
            server: { baseDir: [path.resolve(__dirname, 'dist')] },
            open: true
        })
    );
}

const CleanCss = new PurgecssPlugin({
    paths: glob.sync([`./src/**/*.hbs`, `./src/js/*.js`]),
    whitelist: ['active']
});

if (mode === 'none') {
    config.plugins.push(CleanCss);
}

if (inProduction) {
    config.plugins.push(
        new OptimizeCssAssetsPlugin({
            canPrint: true
        }),
        CleanCss
    );
}
module.exports = config;
