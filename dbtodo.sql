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
-- Database: `dbtodo`
--

-- --------------------------------------------------------

--
-- Table structure for table `todo`
--

CREATE TABLE `todo` (
  `id` int(11) NOT NULL,
  `text` varchar(50) DEFAULT NULL,
  `complete` tinyint(1) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `todo`
--

INSERT INTO `todo` (`id`, `text`, `complete`, `user_id`) VALUES
(1, 'Go to the store!', 0, 2),
(3, 'Check the mail.', 1, 2),
(4, 'INSERT TODO', 0, 3),
(5, 'BWAHAHAH', 1, 3),
(8, 'TEST', 1, 3),
(9, 'TEST', 0, 3);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `public_id` varchar(50) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `password` varchar(80) DEFAULT NULL,
  `admin` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `public_id`, `name`, `password`, `admin`) VALUES
(1, '1c89a5cd-1210-4019-9060-c2aa3eb4a227', 'Admin', 'sha256$LjFGulRI$9e49767aab3e52c816ab765f66c6afc59baafedce7ddbf8a3d1ed8aea0fac1f8', 1),
(2, '3d7e5cdd-b4ea-4c67-853f-714b60ad4f25', 'Anthony', 'sha256$sCadl68G$2602b311f66ee204dadc46b244bef6d178c88171eb25f6d1614bce051ca75c0a', 0),
(3, 'f11eccd3-a5ae-497d-98b6-5470f17d6796', 'kyben', 'sha256$GF75n2dN$16c34ece2be01f1ffac3c2e8e3425b3f0fc3fd158eb5cc9f466be8b1e9bc6bb1', 0),
(4, '41272112-6bdf-4abe-ad5c-8aa232ce6466', 'mokong', 'sha256$YBJtbbLC$06debec579319dfdb980e9dbc2807ddd707fc8b749318a00f3e4c44eeccd3c49', 1),
(5, '917f4adb-5c48-49d5-82eb-daab6890ffb6', 'samal', 'sha256$u2NnRoLC$66b3844265f76e3e3ab985196b50ab8003234dbd28bb44b1c59d9b8fbaa1baaa', 0),
(6, '879f42f3-522a-4f5a-bdc0-7c3a9044e8f6', 'hahaha', 'sha256$mCJtuwyi$8f264468f944c40f10d6a8f15086defece7b78223ec6eb4d20e7e336fc7d1979', 0),
(8, 'ccca1d67-2233-4fc5-b0d7-aa5da4fb39ed', 'delete', 'sha256$nzi32lPS$227ac618acdefc578ce1fe5c9585ed5def2ba45740ac706cd9c589330eecf90a', 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `todo`
--
ALTER TABLE `todo`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `todo`
--
ALTER TABLE `todo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
