package com.ashutosh.backend.dto.response;

import lombok.Builder;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@Builder
public class ReviewResponseDTO {
    // Sent to the frontend to display public reviews on a vehicle's page.
    private Long id;
    private Long bookingId;
    private Integer rating;
    private String comment;
    private String reviewerFirstName; // Extracted from the related AppUser for display
    private LocalDateTime createdAt;
    private String reviewerEmail;
}