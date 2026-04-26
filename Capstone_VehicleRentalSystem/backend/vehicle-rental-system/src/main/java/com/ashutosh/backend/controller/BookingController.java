package com.ashutosh.backend.controller;

import com.ashutosh.backend.dto.request.BookingRequestDTO;
import com.ashutosh.backend.dto.response.BookingResponseDTO;
import com.ashutosh.backend.service.BookingService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.security.Principal;
import java.util.List;

@RestController
@RequestMapping("/api/bookings")
@CrossOrigin(origins = "*")
@RequiredArgsConstructor
public class BookingController {

    private final BookingService bookingService;

    @PostMapping
    public ResponseEntity<?> createBooking(@Valid @RequestBody BookingRequestDTO request, Authentication authentication) {
            String userEmail = "";
            Object principal = authentication.getPrincipal();

            if (principal instanceof com.ashutosh.backend.entity.AppUser) {
                userEmail = ((com.ashutosh.backend.entity.AppUser) principal).getEmail();
            } else if (principal instanceof org.springframework.security.core.userdetails.UserDetails) {
                userEmail = ((org.springframework.security.core.userdetails.UserDetails) principal).getUsername();
            } else {
                userEmail = principal.toString();
            }

            BookingResponseDTO response = bookingService.createBooking(request, userEmail);
            return new ResponseEntity<>(response, HttpStatus.CREATED);
    }

    // 2. Get my booking history (Any logged-in user)
    @GetMapping("/my-bookings")
    public ResponseEntity<List<BookingResponseDTO>> getMyBookings(Principal principal) {
        return ResponseEntity.ok(bookingService.getUserBookings(principal.getName()));
    }

    @PutMapping("/{id}/cancel")
    public ResponseEntity<BookingResponseDTO> cancelBooking(@PathVariable Long id, Principal principal) {
        BookingResponseDTO response = bookingService.cancelBooking(id, principal.getName());
        return ResponseEntity.ok(response);
    }

    @GetMapping("/admin/all")
    public ResponseEntity<List<BookingResponseDTO>> getAllBookingsAdmin() {
        return ResponseEntity.ok(bookingService.getAllBookingsForAdmin());
    }
    
    @PutMapping("/admin/{id}/complete")
    public ResponseEntity<BookingResponseDTO> completeBooking(@PathVariable Long id) {
        return ResponseEntity.ok(bookingService.completeBooking(id));
    }
}