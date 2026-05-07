-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 07, 2026 at 10:30 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `antrian`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id_admin` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id_admin`, `username`, `password`) VALUES
(1, 'admin', '12345');

-- --------------------------------------------------------

--
-- Table structure for table `antrian`
--

CREATE TABLE `antrian` (
  `id_antrian` int(11) NOT NULL,
  `nomor` varchar(5) NOT NULL,
  `status` enum('menunggu','dipanggil','selesai') DEFAULT 'menunggu',
  `waktu` datetime DEFAULT current_timestamp(),
  `id_user` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `antrian`
--

INSERT INTO `antrian` (`id_antrian`, `nomor`, `status`, `waktu`, `id_user`) VALUES
(1, 'A001', 'selesai', '2026-04-10 06:56:23', 1),
(2, 'A002', 'dipanggil', '2026-04-10 06:56:37', 2),
(3, 'A003', 'selesai', '2026-04-10 07:03:36', 3),
(4, 'A004', 'selesai', '2026-04-10 07:03:42', 4),
(7, 'A007', 'menunggu', '2026-04-10 07:17:59', 7),
(9, 'A009', 'menunggu', '2026-04-10 07:18:10', 9),
(10, 'A010', 'menunggu', '2026-04-10 07:18:15', 10),
(18, 'A011', 'menunggu', '2026-04-16 00:40:50', 18),
(19, 'A012', 'menunggu', '2026-04-30 22:40:09', 19),
(20, 'A013', 'menunggu', '2026-04-30 22:55:33', 20),
(21, 'A014', 'menunggu', '2026-04-30 22:59:59', 21),
(22, 'A015', 'menunggu', '2026-05-01 00:41:57', 22),
(23, 'A016', 'menunggu', '2026-05-01 00:46:54', 23);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id_user` int(11) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `no_hp` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id_user`, `nama`, `no_hp`) VALUES
(1, 'airlangga', '08'),
(2, 'pangestu', '1'),
(3, 'satria', '892374892'),
(4, 'reyhan', '823947823947'),
(5, 'noer', '8942375'),
(6, 'pelangi', '298235'),
(7, 'spiderman', '34534643'),
(8, 'mantananjing', '2352352'),
(9, 'peter', '2352345'),
(10, 'parker', '36345345'),
(11, 'galau bet', '345345'),
(12, 'kenapa si aku terus', '3245234'),
(13, 'kenapa aku ga seberuntung orang', '23525235'),
(14, 'ya allah', '435634'),
(15, 'aku juga cape', '256346'),
(16, 'apa aku bundir aja', '432653246'),
(17, 'cuman aku takut', '35463564'),
(18, 'tes', '14234'),
(19, 'airlangga', '1'),
(20, 'airlangga', '3'),
(21, 'airlangga', '6'),
(22, 'airlangga', '9'),
(23, 'A', 'F');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id_admin`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `antrian`
--
ALTER TABLE `antrian`
  ADD PRIMARY KEY (`id_antrian`),
  ADD KEY `id_user` (`id_user`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id_user`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id_admin` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `antrian`
--
ALTER TABLE `antrian`
  MODIFY `id_antrian` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id_user` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `antrian`
--
ALTER TABLE `antrian`
  ADD CONSTRAINT `antrian_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `users` (`id_user`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
