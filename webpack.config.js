const path = require('path');

const glob = require('glob-all');

const PurgecssPlugin = require('purgecss-webpack-plugin');

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

const config = {
    mode,
    //entry points
    entry: {
        css: './src/sass/app.scss'
    },

    //destination for trans-piled files
    output: {
        path: path.resolve(__dirname, 'ui'),
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
                //use absolute path to speed up module resolution instead of regular expressions like test:/\.scss$/
                test: path.resolve(__dirname, 'src/sass/app.scss'),
                use: ExtractTextPlugin.extract({
                    fallback: 'style-loader',
                    use: [
                        {
                            loader: 'css-loader',
                            options: {
                                minimize: inProduction
                            }
                        },
                        {
                            loader: 'postcss-loader',
                            options: {
                                ident: 'postcss',
                                plugins: [
                                    new require('autoprefixer')({
                                        browsers: ['>1%', 'last 2 versions'],
                                        // dont add old flexbox spec properties for webkit
                                        flexbox: 'no-2009'
                                    })
                                    // purgecss({
                                    //     content: ['./src/**/*.hbs']
                                    // })
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
        new WebpackNotifier({
            alwaysNotify: true,
            title: 'Compilation was successful',
            contentImage: path.resolve(__dirname, 'andela.png')
        }),
        new CopyWebpackPlugin([
            {
                from: path.resolve(__dirname, 'src/images'),
                to: path.resolve(__dirname, 'ui/images')
            }
        ]),

        new HandlebarsPlugin({
            entry: path.join(__dirname, 'src', 'pages', '*.hbs'),
            output: path.join(__dirname, 'ui', '[name].html'),
            partials: [path.join(__dirname, 'src', 'partials', '*.hbs')],
            onBeforeSave: (Handlebars, resultHtml) => {
                //prettify html
                return pretty(resultHtml);
            }
        }),
        //extract css out of the js modules
        new ExtractTextPlugin('css/app.css'),
        new PurgecssPlugin({
            paths: glob.sync([`./src/**/*.hbs`]),
            rejected: true
        })
    ]
};

if (!inProduction) {
    // add browserSync only in development
    config.plugins.push(
        new BrowserSyncPlugin({
            port: 7000,
            server: { baseDir: [path.resolve(__dirname, 'ui')] },
            open: true
        })
    );
}
module.exports = config;
