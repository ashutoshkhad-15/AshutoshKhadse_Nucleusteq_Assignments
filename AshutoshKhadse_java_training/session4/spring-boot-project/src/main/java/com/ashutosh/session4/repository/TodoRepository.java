package com.ashutosh.session4.repository;

import com.ashutosh.session4.entity.Todo;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

// I added the @Repository annotation here to mark this as our Data Access component
// Spring Data JPA figures this out automatically
// because we are extending JpaRepository, but I kept it to makes the code clearer to anyone reading it
@Repository
public interface TodoRepository extends JpaRepository<Todo, Long> {

    // By simply extending JpaRepository, Spring automatically generates the actual database
    // code behind the scenes for all the standard CRUD operations like save(), findAll(),
    // findById(), deleteById() etc
    //
    // The <Todo, Long> generics are how I'm telling Spring two things:
    // 1. 'Todo': This repository is for managing the Todo entity.
    // 2. 'Long': The primary key (the ID) of the Todo entity is of type Long.
    //
    // I left this body empty for now since the built-in methods cover all our basic needs.
    // But we can add custom query methods here later like 'findByTitle'
}
