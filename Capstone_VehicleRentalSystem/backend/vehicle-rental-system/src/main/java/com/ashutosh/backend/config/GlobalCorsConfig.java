package com.ashutosh.backend.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.Ordered;
import org.springframework.core.annotation.Order;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;
import org.springframework.web.filter.CorsFilter;

@Configuration
public class GlobalCorsConfig {

    // @Order(Ordered.HIGHEST_PRECEDENCE) forces this filter to run BEFORE Spring Security
    @Bean
    @Order(Ordered.HIGHEST_PRECEDENCE)
    public CorsFilter corsFilter() {
        CorsConfiguration config = new CorsConfiguration();

        // Allow any origin (e.g., your Live Server on 127.0.0.1:5500)
        config.addAllowedOriginPattern("*");

        // Allow any header
        config.addAllowedHeader("*");

        // Allow any method (GET, POST, OPTIONS, etc.)
        config.addAllowedMethod("*");

        // Do not enforce credentials for this basic setup
        config.setAllowCredentials(false);

        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", config);

        return new CorsFilter(source);
    }
}