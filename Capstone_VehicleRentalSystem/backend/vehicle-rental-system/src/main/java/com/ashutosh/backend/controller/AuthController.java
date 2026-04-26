package com.ashutosh.backend.controller;

import com.ashutosh.backend.dto.request.LoginRequestDTO;
import com.ashutosh.backend.dto.request.RegisterRequestDTO;
import com.ashutosh.backend.dto.response.LoginResponseDTO;
import com.ashutosh.backend.dto.response.UserResponseDTO;
import com.ashutosh.backend.service.UserService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    private final UserService userService;

    // Constructor Injection
    public AuthController(UserService userService) {
        this.userService = userService;
    }

    // PUBLIC: Create a new user account
    @PostMapping("/register")
    public ResponseEntity<UserResponseDTO> register(@Valid @RequestBody RegisterRequestDTO request) {
        return ResponseEntity.ok(userService.registerUser(request));
    }

    // PUBLIC: Authenticate and get JWT Token
    @PostMapping("/login")
    public ResponseEntity<LoginResponseDTO> login(@Valid @RequestBody LoginRequestDTO request) {
        return ResponseEntity.ok(userService.authenticateUser(request));
    }

    @GetMapping("/me")
    public ResponseEntity<UserResponseDTO> getCurrentUser(org.springframework.security.core.Authentication authentication) {
        String userEmail = "";
        Object principal = authentication.getPrincipal();

        if (principal instanceof com.ashutosh.backend.entity.AppUser) {
            userEmail = ((com.ashutosh.backend.entity.AppUser) principal).getEmail();
        } else if (principal instanceof org.springframework.security.core.userdetails.UserDetails) {
            userEmail = ((org.springframework.security.core.userdetails.UserDetails) principal).getUsername();
        } else {
            userEmail = principal.toString();
        }
        return ResponseEntity.ok(userService.getUserProfile(userEmail));
    }
}