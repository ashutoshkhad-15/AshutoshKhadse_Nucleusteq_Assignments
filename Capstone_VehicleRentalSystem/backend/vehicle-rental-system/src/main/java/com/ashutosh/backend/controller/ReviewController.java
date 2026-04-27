package com.ashutosh.backend.controller;

import com.ashutosh.backend.dto.request.ReviewRequestDTO;
import com.ashutosh.backend.dto.response.ReviewResponseDTO;
import com.ashutosh.backend.service.ReviewService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/reviews")
@CrossOrigin(origins = "*")
@RequiredArgsConstructor
public class ReviewController {

    private final ReviewService reviewService;

    @PostMapping
    public ResponseEntity<ReviewResponseDTO> addReview(
            @Valid @RequestBody ReviewRequestDTO request,
            Authentication authentication) {

        String userEmail = extractEmail(authentication);
        ReviewResponseDTO response = reviewService.addReview(request, userEmail);
        return new ResponseEntity<>(response, HttpStatus.CREATED);
    }

    @GetMapping("/vehicle/{vehicleId}")
    public ResponseEntity<List<ReviewResponseDTO>> getVehicleReviews(@PathVariable Long vehicleId) {
        return ResponseEntity.ok(reviewService.getVehicleReviews(vehicleId));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteReview(@PathVariable Long id, Authentication authentication) {
        String userEmail = extractEmail(authentication);
        reviewService.deleteReview(id, userEmail);
        return ResponseEntity.noContent().build(); // Returns a clean 204 No Content status
    }

    private String extractEmail(Authentication authentication) {
        Object principal = authentication.getPrincipal();
        if (principal instanceof com.ashutosh.backend.entity.AppUser) {
            return ((com.ashutosh.backend.entity.AppUser) principal).getEmail();
        } else if (principal instanceof org.springframework.security.core.userdetails.UserDetails) {
            return ((org.springframework.security.core.userdetails.UserDetails) principal).getUsername();
        } else {
            return principal.toString();
        }
    }
}