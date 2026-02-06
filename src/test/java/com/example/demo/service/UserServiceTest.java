package com.example.demo.service;

import com.example.demo.entity.User;
import com.example.demo.repository.UserRepository;
import com.example.demo.exception.UserNotFoundException;
import com.example.demo.exception.UserAlreadyExistsException;
import jakarta.persistence.EntityManager;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Arrays;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class UserServiceTest {

    @Mock
    private UserRepository userRepository;
    
    @Mock
    private EntityManager entityManager;

    private UserService userService;

    @BeforeEach
    void setUp() {
        userService = new UserService(userRepository, entityManager);
    }

    @Test
    void testGetAllUsers() {
        User user1 = new User();
        user1.setId(1L);
        user1.setName("John Doe");
        user1.setEmail("john@example.com");

        User user2 = new User();
        user2.setId(2L);
        user2.setName("Jane Doe");
        user2.setEmail("jane@example.com");

        List<User> users = Arrays.asList(user1, user2);
        when(userRepository.findAll()).thenReturn(users);

        List<User> result = userService.getAllUsers();

        assertEquals(2, result.size());
        verify(userRepository, times(1)).findAll();
    }

    @Test
    void testGetUserById() {
        User user = new User();
        user.setId(1L);
        user.setName("John Doe");

        when(userRepository.findById(1L)).thenReturn(Optional.of(user));

        Optional<User> result = userService.getUserById(1L);

        assertTrue(result.isPresent());
        assertEquals("John Doe", result.get().getName());
        verify(userRepository, times(1)).findById(1L);
    }

    @Test
    void testGetUserByEmail() {
        User user = new User();
        user.setEmail("john@example.com");
        user.setName("John Doe");

        when(userRepository.findByEmail("john@example.com")).thenReturn(Optional.of(user));

        Optional<User> result = userService.getUserByEmail("john@example.com");

        assertTrue(result.isPresent());
        assertEquals("john@example.com", result.get().getEmail());
        verify(userRepository, times(1)).findByEmail("john@example.com");
    }

    @Test
    void testCreateUser() {
        User user = new User();
        user.setEmail("john@example.com");
        user.setName("John Doe");

        when(userRepository.existsByEmail("john@example.com")).thenReturn(false);
        when(userRepository.save(any(User.class))).thenReturn(user);

        User result = userService.createUser(user);

        assertNotNull(result);
        assertEquals("john@example.com", result.getEmail());
        verify(userRepository, times(1)).existsByEmail("john@example.com");
        verify(userRepository, times(1)).save(user);
    }

    @Test
    void testCreateUserThrowsExceptionWhenUserExists() {
        User user = new User();
        user.setEmail("john@example.com");

        when(userRepository.existsByEmail("john@example.com")).thenReturn(true);

        assertThrows(UserAlreadyExistsException.class, () -> userService.createUser(user));
        verify(userRepository, times(1)).existsByEmail("john@example.com");
        verify(userRepository, never()).save(any(User.class));
    }

    @Test
    void testUpdateUser() {
        User existingUser = new User();
        existingUser.setId(1L);
        existingUser.setName("John Doe");
        existingUser.setEmail("john@example.com");

        User updatedDetails = new User();
        updatedDetails.setName("John Updated");
        updatedDetails.setEmail("john.updated@example.com");
        updatedDetails.setPhone("1234567890");
        updatedDetails.setAddress("123 Main St");

        when(userRepository.findById(1L)).thenReturn(Optional.of(existingUser));
        when(userRepository.save(any(User.class))).thenReturn(existingUser);

        User result = userService.updateUser(1L, updatedDetails);

        assertEquals("John Updated", result.getName());
        assertEquals("john.updated@example.com", result.getEmail());
        verify(userRepository, times(1)).findById(1L);
        verify(userRepository, times(1)).save(existingUser);
    }

    @Test
    void testUpdateUserThrowsExceptionWhenNotFound() {
        User updatedDetails = new User();
        when(userRepository.findById(1L)).thenReturn(Optional.empty());

        assertThrows(UserNotFoundException.class, () -> userService.updateUser(1L, updatedDetails));
        verify(userRepository, times(1)).findById(1L);
        verify(userRepository, never()).save(any(User.class));
    }

    @Test
    void testDeleteUser() {
        User user = new User();
        user.setId(1L);

        when(userRepository.findById(1L)).thenReturn(Optional.of(user));

        userService.deleteUser(1L);

        verify(userRepository, times(1)).findById(1L);
        verify(userRepository, times(1)).delete(user);
    }

    @Test
    void testDeleteUserThrowsExceptionWhenNotFound() {
        when(userRepository.findById(1L)).thenReturn(Optional.empty());

        assertThrows(UserNotFoundException.class, () -> userService.deleteUser(1L));
        verify(userRepository, times(1)).findById(1L);
        verify(userRepository, never()).delete(any(User.class));
    }

    @Test
    void testHashPassword() {
        String password = "mySecurePassword123";
        String hashedPassword = userService.hashPassword(password);

        assertNotNull(hashedPassword);
        assertNotEquals(password, hashedPassword);
        assertTrue(hashedPassword.startsWith("$2a$"));
    }

    @Test
    void testVerifyPassword() {
        String password = "mySecurePassword123";
        String hashedPassword = userService.hashPassword(password);

        assertTrue(userService.verifyPassword(password, hashedPassword));
        assertFalse(userService.verifyPassword("wrongPassword", hashedPassword));
    }

    @Test
    void testGeneratePasswordResetToken() {
        String token = userService.generatePasswordResetToken();

        assertNotNull(token);
        assertEquals(64, token.length());
    }

    @Test
    void testParseUserDataXml() {
        String xmlContent = "<user><name>John Doe</name></user>";
        String result = userService.parseUserDataXml(xmlContent);

        assertNotNull(result);
        assertEquals("John Doe", result);
    }

    @Test
    void testParseUserDataXmlWithInvalidXml() {
        String invalidXml = "<user><name>John Doe</user>";
        
        assertThrows(com.example.demo.exception.XmlParsingException.class, 
            () -> userService.parseUserDataXml(invalidXml));
    }

    // Test removed: searchUsersByName is deprecated and private
    // It was a demo method for SQL injection protection that required external database setup

    // Tests removed: readUserFile methods were demo vulnerability code that couldn't be properly tested

    @Test
    void testProcessUserDataWithValidData() {
        assertDoesNotThrow(() -> userService.processUserData("12345"));
    }

    @Test
    void testProcessUserDataWithInvalidData() {
        assertThrows(IllegalArgumentException.class, 
            () -> userService.processUserData("invalid"));
    }

    @Test
    void testGenerateSessionId() {
        String sessionId1 = userService.generateSessionId();
        String sessionId2 = userService.generateSessionId();

        assertNotNull(sessionId1);
        assertNotNull(sessionId2);
        assertFalse(sessionId1.isEmpty());
        assertFalse(sessionId2.isEmpty());
    }
}
