package com.ashutosh.backend;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;

/**
 * Main entry point for the Vehicle Rental System.
 * Configures the Spring Boot environment and enables JPA auditing to
 * automatically track when database records are created or updated.
 */
@EnableJpaAuditing
@SpringBootApplication
public class VehicleRentalSystemApplication {

	/**
	 * Starts the application and initializes the Spring framework.
	 * This method launches the main server process and prepares the application context.
	 * * @param args Command line arguments provided at startup.
	 */
	public static void main(String[] args) {
		SpringApplication.run(VehicleRentalSystemApplication.class, args);
	}

}