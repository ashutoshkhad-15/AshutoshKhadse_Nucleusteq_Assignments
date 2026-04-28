package com.ashutosh.backend.controller;

import com.ashutosh.backend.dto.request.LoginRequestDTO;
import com.ashutosh.backend.dto.request.RegisterRequestDTO;
import com.ashutosh.backend.dto.response.LoginResponseDTO;
import com.ashutosh.backend.dto.response.UserResponseDTO;
import com.ashutosh.backend.service.UserService;
import jakarta.validation.Valid;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

/**
 * REST controller responsible for handling authentication endpoints.
 * Manages incoming HTTP requests for user registration, login, and session validation.
 */
@RestController
@RequestMapping("/api/auth")
@Slf4j
public class AuthController {

    private final UserService userService;

    /**
     * Constructor used to inject the UserService dependency.
     */
    public AuthController(UserService userService) {
        this.userService = userService;
    }

    /**
     * Processes a public request to create a new user account.
     *
     * @param request The data transfer object containing registration details.
     * @return ResponseEntity containing the newly created user data.
     */
    @PostMapping("/register")
    public ResponseEntity<UserResponseDTO> register(@Valid @RequestBody RegisterRequestDTO request) {
        log.info("REST request received: Register new user with email: {}", request.getEmail());

        UserResponseDTO response = userService.registerUser(request);

        log.info("Successfully processed registration request. Returned user ID: {}", response.getId());
        return ResponseEntity.ok(response);
    }

    /**
     * Processes a public request to authenticate a user.
     * Returns a JWT token if the credentials are valid.
     *
     * @param request The data transfer object containing login credentials.
     * @return ResponseEntity containing the JWT token and basic user details.
     */
    @PostMapping("/login")
    public ResponseEntity<LoginResponseDTO> login(@Valid @RequestBody LoginRequestDTO request) {
        log.info("REST request received: Authenticate user with email: {}", request.getEmail());

        LoginResponseDTO response = userService.authenticateUser(request);

        log.info("Successfully authenticated user: {}. Returning JWT token.", request.getEmail());
        return ResponseEntity.ok(response);
    }

    /**
     * Retrieves the profile details of the currently logged-in user.
     * Extracts the user's email directly from the active Spring Security context.
     *
     * @param authentication The current security context injected by Spring.
     * @return ResponseEntity containing the authenticated user's profile data.
     */
    @GetMapping("/me")
    public ResponseEntity<UserResponseDTO> getCurrentUser(Authentication authentication) {
        String userEmail = "";
        Object principal = authentication.getPrincipal();

        // Safely extract the email based on how Spring Security stored the principal
        if (principal instanceof com.ashutosh.backend.entity.AppUser) {
            userEmail = ((com.ashutosh.backend.entity.AppUser) principal).getEmail();
        } else if (principal instanceof org.springframework.security.core.userdetails.UserDetails) {
            userEmail = ((org.springframework.security.core.userdetails.UserDetails) principal).getUsername();
        } else {
            userEmail = principal.toString();
        }

        log.info("REST request received: Fetch profile for authenticated user: {}", userEmail);

        UserResponseDTO response = userService.getUserProfile(userEmail);
        return ResponseEntity.ok(response);
    }
}