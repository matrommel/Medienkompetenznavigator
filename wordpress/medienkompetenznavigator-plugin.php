<?php
/*
Plugin Name: b3_Medienkompetenznavigator
Description: Ein Plugin zur Darstellung von Medienkompetenzinformationen.
Version: 0.1
Author: Rommel
*/

// Register and enqueue the CSS and JS files
function medienkompetenznavigator_enqueue_scripts() {
    // Register the CSS file
    wp_register_style('medienkompetenznavigator-style', plugins_url('medienkompetenznavigator-style.css', __FILE__));
    // Enqueue the CSS file
    wp_enqueue_style('medienkompetenznavigator-style');

    // Register the jQuery UI CSS file
    wp_register_style('jquery-ui-css', 'https://code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css');
    // Enqueue the jQuery UI CSS file
    wp_enqueue_style('jquery-ui-css');

    // Register the jQuery library
    wp_register_script('jquery', 'https://code.jquery.com/jquery-3.6.0.min.js');
    // Enqueue the jQuery library
    wp_enqueue_script('jquery');

    // Register the jQuery UI library
    wp_register_script('jquery-ui', 'https://code.jquery.com/ui/1.12.1/jquery-ui.min.js');
    // Enqueue the jQuery UI library
    wp_enqueue_script('jquery-ui');

    // Register the JS file
    wp_register_script('medienkompetenznavigator-script', plugins_url('medienkompetenznavigator-script.js', __FILE__), array('jquery', 'jquery-ui'), null, true);
    // Enqueue the JS file
    wp_enqueue_script('medienkompetenznavigator-script');

    // Localize the script with the JSON URL
    wp_localize_script('medienkompetenznavigator-script', 'medienkompetenznavigator_vars', array(
        'json_url' => plugins_url('data.json', __FILE__) // Adjust the path to your JSON file
    ));
}
add_action('wp_enqueue_scripts', 'medienkompetenznavigator_enqueue_scripts');

// Shortcode to display the accordion
function medienkompetenznavigator_shortcode() {
    return '<div id="accordion"></div>';
}
add_shortcode('medienkompetenznavigator', 'medienkompetenznavigator_shortcode');
?>