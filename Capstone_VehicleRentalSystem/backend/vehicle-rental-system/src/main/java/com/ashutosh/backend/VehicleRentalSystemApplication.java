package com.ashutosh.backend;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;

@EnableJpaAuditing
@SpringBootApplication
public class VehicleRentalSystemApplication {

	public static void main(String[] args) {
		SpringApplication.run(VehicleRentalSystemApplication.class, args);
	}

}
