package com.example.demo.controller;

import com.example.demo.entity.User;
import com.example.demo.service.UserService;
import com.example.demo.exception.UserNotFoundException;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import java.util.Arrays;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class UserControllerTest {

    @Mock
    private UserService userService;

    private UserController userController;

    @BeforeEach
    void setUp() {
        userController = new UserController(userService);
    }

    @Test
    void testGetAllUsers() {
        User user1 = new User();
        user1.setId(1L);
        user1.setName("John Doe");
        
        User user2 = new User();
        user2.setId(2L);
        user2.setName("Jane Doe");

        List<User> users = Arrays.asList(user1, user2);
        when(userService.getAllUsers()).thenReturn(users);

        ResponseEntity<List<User>> response = userController.getAllUsers();

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(2, response.getBody().size());
        verify(userService, times(1)).getAllUsers();
    }

    @Test
    void testGetUserByIdFound() {
        User user = new User();
        user.setId(1L);
        user.setName("John Doe");

        when(userService.getUserById(1L)).thenReturn(Optional.of(user));

        ResponseEntity<User> response = userController.getUserById(1L);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals("John Doe", response.getBody().getName());
        verify(userService, times(1)).getUserById(1L);
    }

    @Test
    void testGetUserByIdNotFound() {
        when(userService.getUserById(1L)).thenReturn(Optional.empty());

        ResponseEntity<User> response = userController.getUserById(1L);

        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
        assertNull(response.getBody());
        verify(userService, times(1)).getUserById(1L);
    }

    @Test
    void testGetUserByEmailFound() {
        User user = new User();
        user.setEmail("john@example.com");
        user.setName("John Doe");

        when(userService.getUserByEmail("john@example.com")).thenReturn(Optional.of(user));

        ResponseEntity<User> response = userController.getUserByEmail("john@example.com");

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals("john@example.com", response.getBody().getEmail());
        verify(userService, times(1)).getUserByEmail("john@example.com");
    }

    @Test
    void testGetUserByEmailNotFound() {
        when(userService.getUserByEmail("notfound@example.com")).thenReturn(Optional.empty());

        ResponseEntity<User> response = userController.getUserByEmail("notfound@example.com");

        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
        assertNull(response.getBody());
        verify(userService, times(1)).getUserByEmail("notfound@example.com");
    }

    @Test
    void testCreateUser() {
        User user = new User();
        user.setName("John Doe");
        user.setEmail("john@example.com");

        when(userService.createUser(any(User.class))).thenReturn(user);

        ResponseEntity<User> response = userController.createUser(user);

        assertEquals(HttpStatus.CREATED, response.getStatusCode());
        assertEquals("john@example.com", response.getBody().getEmail());
        verify(userService, times(1)).createUser(user);
    }

    @Test
    void testUpdateUserFound() {
        User existingUser = new User();
        existingUser.setId(1L);
        existingUser.setName("John Updated");

        User updateDetails = new User();
        updateDetails.setName("John Updated");

        when(userService.updateUser(eq(1L), any(User.class))).thenReturn(existingUser);

        ResponseEntity<User> response = userController.updateUser(1L, updateDetails);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals("John Updated", response.getBody().getName());
        verify(userService, times(1)).updateUser(eq(1L), any(User.class));
    }

    @Test
    void testUpdateUserNotFound() {
        User updateDetails = new User();
        updateDetails.setName("John Updated");

        when(userService.updateUser(eq(1L), any(User.class))).thenThrow(new UserNotFoundException("User not found"));

        ResponseEntity<User> response = userController.updateUser(1L, updateDetails);

        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
        verify(userService, times(1)).updateUser(eq(1L), any(User.class));
    }

    @Test
    void testDeleteUser() {
        doNothing().when(userService).deleteUser(1L);

        ResponseEntity<Void> response = userController.deleteUser(1L);

        assertEquals(HttpStatus.NO_CONTENT, response.getStatusCode());
        verify(userService, times(1)).deleteUser(1L);
    }

    @Test
    void testDeleteUserNotFound() {
        doThrow(new UserNotFoundException("User not found")).when(userService).deleteUser(1L);

        ResponseEntity<Void> response = userController.deleteUser(1L);

        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
        verify(userService, times(1)).deleteUser(1L);
    }

    @Test
    void testCreateUserWithException() {
        User user = new User();
        user.setName("John Doe");
        user.setEmail("invalid");

        when(userService.createUser(any(User.class))).thenThrow(new RuntimeException("Validation error"));

        ResponseEntity<User> response = userController.createUser(user);

        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
        assertNull(response.getBody());
        verify(userService, times(1)).createUser(user);
    }

    @Test
    void testReadFileNotFound() {
        // Test IOException handling for non-existent file
        ResponseEntity<String> response = userController.readFile("nonexistent.txt");

        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
        assertNull(response.getBody());
    }

    @Test
    void testReadFilePathTraversalBlocked() {
        // Test that path traversal attempts are rejected
        ResponseEntity<String> response = userController.readFile("../../../etc/passwd");

        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
        assertNull(response.getBody());
    }

    @Test
    void testSearchUsersByName() {
        User user = new User();
        user.setId(1L);
        user.setName("John Doe");

        List<User> users = Arrays.asList(user);
        when(userService.searchUsersByName("John Doe")).thenReturn(users);

        ResponseEntity<List<User>> response = userController.searchUsersByName("John Doe");

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(1, response.getBody().size());
        verify(userService, times(1)).searchUsersByName("John Doe");
    }
}
