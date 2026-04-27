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

@Component
public class JwtAuthenticationFilter extends OncePerRequestFilter {

    private final JwtService jwtService;
    private final AppUserRepository userRepository;

    public JwtAuthenticationFilter(JwtService jwtService, AppUserRepository userRepository) {
        this.jwtService = jwtService;
        this.userRepository = userRepository;
    }

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
