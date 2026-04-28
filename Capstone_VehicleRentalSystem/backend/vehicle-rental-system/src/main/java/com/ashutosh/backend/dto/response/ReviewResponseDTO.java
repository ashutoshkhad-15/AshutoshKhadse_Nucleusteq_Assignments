package com.ashutosh.backend.dto.response;

import lombok.Builder;
import lombok.Data;
import java.time.LocalDateTime;

/**
 * Data Transfer Object for presenting vehicle reviews to the client.
 * Provides a read-only view of customer feedback, including the reviewer's
 * identity and the rating, to be displayed on vehicle catalog or detail pages.
 */
@Data
@Builder
public class ReviewResponseDTO {
    // Sent to the frontend to display public reviews on a vehicle's page.
    private Long id;
    private Long bookingId;
    private Integer rating;
    private String comment;
    private String reviewerFirstName;
    private LocalDateTime createdAt;
    private String reviewerEmail;
}