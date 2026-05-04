package com.ashutosh.backend.config;

import com.ashutosh.backend.security.JwtAuthenticationFilter;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

/**
 * Configures the main security policies for the application.
 * Sets up stateless session management, defines role-based access control (RBAC) routing,
 * and integrates the custom JWT validation filter to secure all API endpoints.
 */
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    private final JwtAuthenticationFilter jwtAuthFilter;

    public SecurityConfig(JwtAuthenticationFilter jwtAuthFilter) {
        this.jwtAuthFilter = jwtAuthFilter;
    }

    /**
     * Defines the cryptographic hashing mechanism for the system.
     * Uses BCrypt to securely encode passwords, ensuring raw credentials
     * are never stored or compared in plain text.
     *
     * @return The configured BCrypt password encoder instance.
     */
    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder(); // Mathematically secures the passwords
    }

    /**
     * Builds the primary security filter chain to evaluate incoming HTTP requests.
     * Disables CSRF protection because the REST API relies on stateless JWTs rather than session cookies.
     * Enforces strict access rules:
     * 1. Permits open access for CORS pre-flight requests, authentication, and public catalog viewing.
     * 2. Restricts inventory modifications (POST/PUT/DELETE) and admin booking routes exclusively to the ADMIN role.
     * 3. Mandates a valid authentication token for all other system operations.
     * Inserts the custom JWT filter to intercept and validate tokens before standard Spring security checks.
     *
     * @param http The HttpSecurity builder used to configure web-based security.
     * @return The finalized security filter chain ready for execution.
     * @throws Exception If an error occurs during the security configuration process.
     */
    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
                .csrf(AbstractHttpConfigurer::disable) // Required for stateless REST APIs
                .sessionManagement(session -> session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
                .authorizeHttpRequests(auth -> auth

                        .requestMatchers(HttpMethod.OPTIONS, "/**").permitAll()
                        .requestMatchers("/api/auth/register", "/api/auth/login").permitAll()

                        // PUBLIC: Anyone can view the vehicle catalog
                        .requestMatchers(HttpMethod.GET, "/api/vehicles/admin/**").permitAll()

                        // ADMIN ONLY: Adding/Deleting cars and viewing all bookings
                        .requestMatchers(HttpMethod.POST, "/api/vehicles/**").hasRole("ADMIN")
                        .requestMatchers(HttpMethod.PUT, "/api/vehicles/**").hasRole("ADMIN")
                        .requestMatchers(HttpMethod.DELETE, "/api/vehicles/**").hasRole("ADMIN")
                        .requestMatchers("/api/bookings/admin/**").hasRole("ADMIN")

                        .requestMatchers(HttpMethod.GET, "/api/vehicles/**").permitAll()
                        .requestMatchers(HttpMethod.GET, "/api/reviews/vehicle/**").permitAll()

                        .anyRequest().authenticated()
                )
                // Inject custom JWT Filter before the standard Spring security checks
                .addFilterBefore(jwtAuthFilter, UsernamePasswordAuthenticationFilter.class);

        return http.build();
    }
}