-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: 172.20.0.4
-- Generation Time: Feb 01, 2019 at 09:35 AM
-- Server version: 5.7.23
-- PHP Version: 7.2.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `dbapi`
--

-- --------------------------------------------------------

--
-- Table structure for table `alembic_version`
--

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `alembic_version`
--

INSERT INTO `alembic_version` (`version_num`) VALUES
('6e7a22428e33');

-- --------------------------------------------------------

--
-- Table structure for table `blacklist_tokens`
--

CREATE TABLE `blacklist_tokens` (
  `id` int(11) NOT NULL,
  `token` varchar(500) NOT NULL,
  `blacklisted_on` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `blacklist_tokens`
--

INSERT INTO `blacklist_tokens` (`id`, `token`, `blacklisted_on`) VALUES
(1, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEsImV4cCI6MTU0OTA5NDg0MCwiaWF0IjoxNTQ5MDA4NDM1fQ.mMVumnJYIVJBATBKZsBK5Nx8_EaG391Cm0N24QPr_40', '2019-02-01 16:12:28'),
(2, 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NDkwOTUxNzIsImlhdCI6MTU0OTAwODc2Nywic3ViIjoxfQ.sV12f9dENnefYV19wFeT-xufwKGlOfIURmFL9txVUMw', '2019-02-01 16:13:08'),
(3, 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NDkwMTAyNTUsInN1YiI6MSwiZXhwIjoxNTQ5MDk2NjYwfQ.gyN9oRanGFj4L3A7aWb_um9aidD-5rLfbEfVI5L6xNA', '2019-02-01 16:38:11');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `email` varchar(255) NOT NULL,
  `registered_on` datetime NOT NULL,
  `admin` tinyint(1) NOT NULL,
  `public_id` varchar(100) DEFAULT NULL,
  `username` varchar(50) DEFAULT NULL,
  `password_hash` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `email`, `registered_on`, `admin`, `public_id`, `username`, `password_hash`) VALUES
(1, 'email@email.com', '2019-02-01 07:51:48', 1, '0b110603-0bb5-4eaa-b8e7-fe93a6b0b082', 'kyben', '$2b$12$Os0kEEAjlr1P3dmKmMTKReWeRCiOSod43BoO7fCFBVlobI6JbNigG'),
(2, 'email1@email.com', '2019-02-01 08:30:05', 1, 'c6722fe5-4f02-443a-9675-12cf1f9133fc', 'kyben1', '$2b$12$ZiggkYppVghpw3fuWc0lvODWtYI9m2Qg9hJF/SKYdNHiv7WiV.uAC'),
(3, 'email2@email.com', '2019-02-01 08:32:21', 1, '38962e9a-3430-449c-970d-473e234f39fb', 'kyben2', '$2b$12$b7Jc4iYNhbJRDgsKzVQxruMGKO9T4qUw0xqf1BoSN6JncT5nDQy9y');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `alembic_version`
--
ALTER TABLE `alembic_version`
  ADD PRIMARY KEY (`version_num`);

--
-- Indexes for table `blacklist_tokens`
--
ALTER TABLE `blacklist_tokens`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `token` (`token`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `public_id` (`public_id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `blacklist_tokens`
--
ALTER TABLE `blacklist_tokens`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
