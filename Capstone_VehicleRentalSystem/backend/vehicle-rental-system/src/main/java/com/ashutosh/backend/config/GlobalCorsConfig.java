package com.ashutosh.backend.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.Ordered;
import org.springframework.core.annotation.Order;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;
import org.springframework.web.filter.CorsFilter;

/**
 * Configures Cross-Origin Resource Sharing (CORS) for the application.
 * This setup allows the frontend to communicate with the backend API
 * even when they are running on different ports or domains.
 */
@Configuration
public class GlobalCorsConfig {

    /**
     * Defines a global CORS filter with the highest priority.
     * Setting the order to HIGHEST_PRECEDENCE ensures that CORS pre-flight requests
     * are handled before Spring Security filters. It allows all origins, headers,
     * and HTTP methods to ensure smooth communication during development.
     *
     * @return A configured CorsFilter applied to all application paths.
     */
    @Bean
    @Order(Ordered.HIGHEST_PRECEDENCE)
    public CorsFilter corsFilter() {
        CorsConfiguration config = new CorsConfiguration();

        // Allows requests from any origin
        config.addAllowedOriginPattern("*");

        // Allows all HTTP headers in requests
        config.addAllowedHeader("*");

        // Allows all HTTP methods like GET, POST, PUT, and DELETE
        config.addAllowedMethod("*");

        // Disables credentials to keep the basic setup simple and compatible with wildcards
        config.setAllowCredentials(false);

        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", config);

        return new CorsFilter(source);
    }
}