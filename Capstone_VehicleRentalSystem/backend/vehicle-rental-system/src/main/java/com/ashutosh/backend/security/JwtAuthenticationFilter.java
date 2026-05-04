package com.ashutosh.backend.security;

import com.ashutosh.backend.entity.AppUser;
import com.ashutosh.backend.repository.AppUserRepository;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.lang.NonNull;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.web.authentication.WebAuthenticationDetailsSource;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.util.Collections;

/**
 * Intercepts incoming HTTP requests to validate JSON Web Tokens (JWT).
 * Ensures that only authenticated and active users gain access to protected system endpoints.
 */
@Component
public class JwtAuthenticationFilter extends OncePerRequestFilter {

    private final JwtService jwtService;
    private final AppUserRepository userRepository;

    /**
     * Initializes the filter with required services for token validation and user lookups.
     *
     * @param jwtService The service handling token extraction and verification.
     * @param userRepository The database repository for user data retrieval.
     */
    public JwtAuthenticationFilter(JwtService jwtService, AppUserRepository userRepository) {
        this.jwtService = jwtService;
        this.userRepository = userRepository;
    }

    /**
     * Processes the HTTP request to extract and verify the authorization token.
     * Executes the following core security checks:
     * 1. Header Check: Skips filtering if the request lacks a valid "Bearer" token.
     * 2. Safe Extraction: Parses the token for an email, catching errors to prevent server crashes on malformed data.
     * 3. Database Audit: Verifies the user exists and is actively permitted to use the system (not banned).
     * 4. Signature Verification: Confirms the token mathematically matches the user's secure signature.
     * * If all validations pass, applies the required Spring Security "ROLE_" prefix and authorizes
     * the user for the current request cycle.
     *
     * @param request The incoming HTTP request.
     * @param response The outgoing HTTP response.
     * @param filterChain The chain of filters to continue execution after processing.
     * @throws ServletException If a servlet-specific error occurs during filtering.
     * @throws IOException If an input or output error occurs during the request process.
     */
    @Override
    protected void doFilterInternal(
            @NonNull HttpServletRequest request,
            @NonNull HttpServletResponse response,
            @NonNull FilterChain filterChain
    ) throws ServletException, IOException {

        final String authHeader = request.getHeader("Authorization");

        // Skip if no token is provided in the request
        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            filterChain.doFilter(request, response);
            return;
        }

        final String jwt = authHeader.substring(7);
        String userEmail = null;

        // Extract safely (Prevents server crash if token is malformed)
        try {
            userEmail = jwtService.extractEmail(jwt);
        } catch (Exception e) {
            filterChain.doFilter(request, response);
            return;
        }

        // Authenticate if valid and not already authenticated in this context
        if (userEmail != null && SecurityContextHolder.getContext().getAuthentication() == null) {

            AppUser user = userRepository.findByEmail(userEmail).orElse(null);

            // Ensure user exists, is NOT banned (isActive), and token is mathematically valid
            if (user != null
                    && user.getIsActive()
                    && jwtService.isTokenValid(jwt, user.getEmail())) {

                // Spring Security requires the "ROLE_" prefix to match .hasRole() in the config
                SimpleGrantedAuthority authority =
                        new SimpleGrantedAuthority("ROLE_" + user.getRole().name());

                UsernamePasswordAuthenticationToken authToken =
                        new UsernamePasswordAuthenticationToken(
                                user,
                                null,
                                Collections.singletonList(authority)
                        );

                authToken.setDetails(
                        new WebAuthenticationDetailsSource().buildDetails(request)
                );

                // Officially log the user in for this specific HTTP request
                SecurityContextHolder.getContext().setAuthentication(authToken);
            }
        }

        // Continue the chain to the Controller
        filterChain.doFilter(request, response);
    }
}