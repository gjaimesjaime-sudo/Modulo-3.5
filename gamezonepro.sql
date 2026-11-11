-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 10-11-2026 a las 00:32:16
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `gamezonepro`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `api_tokens`
--

CREATE TABLE `api_tokens` (
  `id_token` bigint(20) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `token_hash` char(64) NOT NULL,
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp(),
  `fecha_expiracion` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `api_tokens`
--

INSERT INTO `api_tokens` (`id_token`, `id_usuario`, `token_hash`, `fecha_creacion`, `fecha_expiracion`) VALUES
(1, 1, 'e452e6cbeb02dca0a20acf912691de5b91d533df98e5e3146aac70e706f2b4cd', '2026-11-05 15:23:07', '2026-11-12 16:23:07'),
(2, 1, 'c6574c9d446babe96449d6b50cec819085bf4c4caeb8563ce2fb76a06cc3026b', '2026-11-05 16:06:35', '2026-11-12 17:06:35'),
(3, 1, 'b17bc0a5b08d29c64cf22fde90773a3dc6c1e36812137cb2ba2f61e0a744ea75', '2026-11-05 16:09:20', '2026-11-12 17:09:20'),
(4, 1, '1633c14b644ae74d6b08d964c257f179370cf57da9e9c7c60932d7f47253b547', '2026-11-09 23:19:59', '2026-11-17 00:19:59');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `historial_elo`
--

CREATE TABLE `historial_elo` (
  `id_historial` int(11) NOT NULL,
  `id_jugador` int(11) NOT NULL,
  `id_resultado` int(11) DEFAULT NULL,
  `elo_anterior` int(11) NOT NULL,
  `elo_nuevo` int(11) NOT NULL,
  `cambio` int(11) NOT NULL,
  `fecha_cambio` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inscripciones`
--

CREATE TABLE `inscripciones` (
  `id_inscripcion` int(11) NOT NULL,
  `id_torneo` int(11) NOT NULL,
  `id_jugador` int(11) NOT NULL,
  `fecha_inscripcion` timestamp NOT NULL DEFAULT current_timestamp(),
  `estado` enum('inscrito','confirmado','retirado','descalificado') DEFAULT 'inscrito'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `jugadores`
--

CREATE TABLE `jugadores` (
  `id_jugador` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `nickname` varchar(15) NOT NULL,
  `elo` int(11) NOT NULL DEFAULT 1000,
  `victorias` int(10) UNSIGNED DEFAULT 0,
  `derrotas` int(10) UNSIGNED DEFAULT 0,
  `empates` int(10) UNSIGNED DEFAULT 0,
  `partidas_jugadas` int(10) UNSIGNED DEFAULT 0,
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `jugadores`
--

INSERT INTO `jugadores` (`id_jugador`, `id_usuario`, `nickname`, `elo`, `victorias`, `derrotas`, `empates`, `partidas_jugadas`, `fecha_creacion`) VALUES
(1, 1, 'Phantom_01', 1000, 0, 0, 0, 0, '2026-11-05 15:19:22');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `mensajes`
--

CREATE TABLE `mensajes` (
  `id_mensaje` bigint(20) NOT NULL,
  `id_remitente` int(11) NOT NULL,
  `id_destinatario` int(11) NOT NULL,
  `contenido` text NOT NULL,
  `fecha_envio` timestamp NOT NULL DEFAULT current_timestamp(),
  `leido` tinyint(1) DEFAULT 0,
  `fecha_lectura` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `permisos`
--

CREATE TABLE `permisos` (
  `id_permiso` int(11) NOT NULL,
  `nombre_permiso` varchar(60) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `permisos`
--

INSERT INTO `permisos` (`id_permiso`, `nombre_permiso`, `descripcion`) VALUES
(1, 'gestionar_usuarios', 'Crear, modificar y eliminar usuarios'),
(2, 'gestionar_jugadores', 'Administrar perfiles de jugadores'),
(3, 'crear_torneos', 'Crear torneos'),
(4, 'editar_torneos', 'Modificar torneos'),
(5, 'eliminar_torneos', 'Eliminar torneos'),
(6, 'inscribirse_torneos', 'Inscribirse en torneos'),
(7, 'retirarse_torneos', 'Retirarse de torneos'),
(8, 'gestionar_inscripciones', 'Administrar inscripciones'),
(9, 'consultar_ranking', 'Consultar clasificación general'),
(10, 'gestionar_ranking', 'Modificar posiciones y puntuaciones'),
(11, 'consultar_perfil', 'Consultar perfiles'),
(12, 'editar_perfil_propio', 'Editar el propio perfil'),
(13, 'consultar_historial_elo', 'Consultar historial ELO'),
(14, 'gestionar_resultados', 'Registrar y modificar resultados'),
(15, 'consultar_resultados', 'Consultar resultados de partidas'),
(16, 'enviar_mensajes', 'Enviar mensajes'),
(17, 'recibir_mensajes', 'Recibir mensajes'),
(18, 'moderar_mensajes', 'Moderar conversaciones'),
(19, 'consultar_estadisticas', 'Consultar estadísticas'),
(20, 'gestionar_configuracion', 'Modificar configuración del sistema');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ranking`
--

CREATE TABLE `ranking` (
  `id_ranking` int(11) NOT NULL,
  `id_jugador` int(11) NOT NULL,
  `posicion` int(11) DEFAULT NULL,
  `puntos_elo` int(11) NOT NULL DEFAULT 1000,
  `victorias` int(10) UNSIGNED DEFAULT 0,
  `derrotas` int(10) UNSIGNED DEFAULT 0,
  `empates` int(10) UNSIGNED DEFAULT 0,
  `partidas_jugadas` int(10) UNSIGNED DEFAULT 0,
  `actualizado` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `ranking`
--

INSERT INTO `ranking` (`id_ranking`, `id_jugador`, `posicion`, `puntos_elo`, `victorias`, `derrotas`, `empates`, `partidas_jugadas`, `actualizado`) VALUES
(1, 1, NULL, 1000, 0, 0, 0, 0, '2026-11-05 15:19:22');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `resultados`
--

CREATE TABLE `resultados` (
  `id_resultado` int(11) NOT NULL,
  `id_torneo` int(11) DEFAULT NULL,
  `id_jugador1` int(11) NOT NULL,
  `id_jugador2` int(11) NOT NULL,
  `id_ganador` int(11) DEFAULT NULL,
  `puntos_jugador1` decimal(6,2) DEFAULT 0.00,
  `puntos_jugador2` decimal(6,2) DEFAULT 0.00,
  `estado` enum('pendiente','finalizado','cancelado') DEFAULT 'pendiente',
  `fecha_partida` datetime DEFAULT current_timestamp(),
  `observaciones` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `roles`
--

CREATE TABLE `roles` (
  `id_rol` int(11) NOT NULL,
  `nombre_rol` varchar(30) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `roles`
--

INSERT INTO `roles` (`id_rol`, `nombre_rol`, `descripcion`) VALUES
(1, 'administrador', 'Control total de GameZone Pro'),
(2, 'usuario', 'Acceso de jugador a GameZone Pro');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rol_permisos`
--

CREATE TABLE `rol_permisos` (
  `id_rol` int(11) NOT NULL,
  `id_permiso` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `rol_permisos`
--

INSERT INTO `rol_permisos` (`id_rol`, `id_permiso`) VALUES
(1, 1),
(1, 2),
(1, 3),
(1, 4),
(1, 5),
(1, 6),
(1, 7),
(1, 8),
(1, 9),
(1, 10),
(1, 11),
(1, 12),
(1, 13),
(1, 14),
(1, 15),
(1, 16),
(1, 17),
(1, 18),
(1, 19),
(1, 20),
(2, 6),
(2, 7),
(2, 9),
(2, 11),
(2, 12),
(2, 13),
(2, 15),
(2, 16),
(2, 17);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `torneos`
--

CREATE TABLE `torneos` (
  `id_torneo` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `juego` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `formato` enum('eliminacion_simple','eliminacion_doble','round_robin','suizo') DEFAULT 'eliminacion_simple',
  `max_jugadores` int(10) UNSIGNED NOT NULL DEFAULT 16,
  `fecha_inicio` datetime NOT NULL,
  `fecha_fin` datetime DEFAULT NULL,
  `estado` enum('proximo','inscripciones','en_curso','finalizado','cancelado') DEFAULT 'inscripciones',
  `id_creador` int(11) DEFAULT NULL,
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `torneos`
--

INSERT INTO `torneos` (`id_torneo`, `nombre`, `juego`, `descripcion`, `formato`, `max_jugadores`, `fecha_inicio`, `fecha_fin`, `estado`, `id_creador`, `fecha_creacion`) VALUES
(1, 'Smash Ultimate', 'Super Smash Bros. Ultimate', 'Torneo de demostración.', 'eliminacion_simple', 32, '2026-11-15 18:00:00', NULL, 'inscripciones', NULL, '2026-11-05 14:29:59'),
(2, 'Persona 5 Royal', 'Persona 5 Royal', 'Torneo de demostración.', 'eliminacion_simple', 16, '2026-11-16 19:00:00', NULL, 'inscripciones', NULL, '2026-11-05 14:29:59'),
(3, 'Genshin Impact', 'Genshin Impact', 'Torneo de demostración.', 'suizo', 64, '2026-11-20 16:00:00', NULL, 'inscripciones', NULL, '2026-11-05 14:29:59');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `nombre_usuario` varchar(30) NOT NULL,
  `correo` varchar(120) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `avatar` varchar(255) DEFAULT NULL,
  `biografia` text DEFAULT NULL,
  `fecha_registro` timestamp NOT NULL DEFAULT current_timestamp(),
  `estado` enum('activo','inactivo','bloqueado') DEFAULT 'activo',
  `id_rol` int(11) NOT NULL DEFAULT 2
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `nombre_usuario`, `correo`, `password_hash`, `avatar`, `biografia`, `fecha_registro`, `estado`, `id_rol`) VALUES
(1, 'JugadorPrueba', 'jugadorprueba@gamezonepro.com', '$2y$10$4GsaU0NoDpeHutjI1lsVG.DcRCfdxmgM0K7V85VsIFFyQfMekis6q', NULL, NULL, '2026-11-05 15:19:22', 'activo', 2);

-- --------------------------------------------------------

--
-- Estructura Stand-in para la vista `vista_ranking_general`
-- (Véase abajo para la vista actual)
--
CREATE TABLE `vista_ranking_general` (
`posicion` bigint(21)
,`id_jugador` int(11)
,`nickname` varchar(15)
,`nombre_usuario` varchar(30)
,`puntos_elo` int(11)
,`victorias` int(10) unsigned
,`derrotas` int(10) unsigned
,`empates` int(10) unsigned
,`partidas_jugadas` int(10) unsigned
);

-- --------------------------------------------------------

--
-- Estructura para la vista `vista_ranking_general`
--
DROP TABLE IF EXISTS `vista_ranking_general`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vista_ranking_general`  AS SELECT row_number() over ( order by `j`.`elo` desc,`j`.`victorias` desc,`j`.`nickname`) AS `posicion`, `j`.`id_jugador` AS `id_jugador`, `j`.`nickname` AS `nickname`, `u`.`nombre_usuario` AS `nombre_usuario`, `j`.`elo` AS `puntos_elo`, `j`.`victorias` AS `victorias`, `j`.`derrotas` AS `derrotas`, `j`.`empates` AS `empates`, `j`.`partidas_jugadas` AS `partidas_jugadas` FROM (`jugadores` `j` join `usuarios` `u` on(`u`.`id_usuario` = `j`.`id_usuario`)) WHERE `u`.`estado` = 'activo' ;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `api_tokens`
--
ALTER TABLE `api_tokens`
  ADD PRIMARY KEY (`id_token`),
  ADD UNIQUE KEY `token_hash` (`token_hash`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `historial_elo`
--
ALTER TABLE `historial_elo`
  ADD PRIMARY KEY (`id_historial`),
  ADD KEY `id_jugador` (`id_jugador`),
  ADD KEY `id_resultado` (`id_resultado`);

--
-- Indices de la tabla `inscripciones`
--
ALTER TABLE `inscripciones`
  ADD PRIMARY KEY (`id_inscripcion`),
  ADD UNIQUE KEY `uq_inscripcion` (`id_torneo`,`id_jugador`),
  ADD KEY `id_jugador` (`id_jugador`);

--
-- Indices de la tabla `jugadores`
--
ALTER TABLE `jugadores`
  ADD PRIMARY KEY (`id_jugador`),
  ADD UNIQUE KEY `id_usuario` (`id_usuario`),
  ADD UNIQUE KEY `nickname` (`nickname`);

--
-- Indices de la tabla `mensajes`
--
ALTER TABLE `mensajes`
  ADD PRIMARY KEY (`id_mensaje`),
  ADD KEY `id_remitente` (`id_remitente`),
  ADD KEY `id_destinatario` (`id_destinatario`);

--
-- Indices de la tabla `permisos`
--
ALTER TABLE `permisos`
  ADD PRIMARY KEY (`id_permiso`),
  ADD UNIQUE KEY `nombre_permiso` (`nombre_permiso`);

--
-- Indices de la tabla `ranking`
--
ALTER TABLE `ranking`
  ADD PRIMARY KEY (`id_ranking`),
  ADD UNIQUE KEY `id_jugador` (`id_jugador`);

--
-- Indices de la tabla `resultados`
--
ALTER TABLE `resultados`
  ADD PRIMARY KEY (`id_resultado`),
  ADD KEY `id_torneo` (`id_torneo`),
  ADD KEY `id_jugador1` (`id_jugador1`),
  ADD KEY `id_jugador2` (`id_jugador2`),
  ADD KEY `id_ganador` (`id_ganador`);

--
-- Indices de la tabla `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id_rol`),
  ADD UNIQUE KEY `nombre_rol` (`nombre_rol`);

--
-- Indices de la tabla `rol_permisos`
--
ALTER TABLE `rol_permisos`
  ADD PRIMARY KEY (`id_rol`,`id_permiso`),
  ADD KEY `id_permiso` (`id_permiso`);

--
-- Indices de la tabla `torneos`
--
ALTER TABLE `torneos`
  ADD PRIMARY KEY (`id_torneo`),
  ADD KEY `id_creador` (`id_creador`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `nombre_usuario` (`nombre_usuario`),
  ADD UNIQUE KEY `correo` (`correo`),
  ADD KEY `fk_usuario_rol` (`id_rol`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `api_tokens`
--
ALTER TABLE `api_tokens`
  MODIFY `id_token` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `historial_elo`
--
ALTER TABLE `historial_elo`
  MODIFY `id_historial` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `inscripciones`
--
ALTER TABLE `inscripciones`
  MODIFY `id_inscripcion` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `jugadores`
--
ALTER TABLE `jugadores`
  MODIFY `id_jugador` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `mensajes`
--
ALTER TABLE `mensajes`
  MODIFY `id_mensaje` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `permisos`
--
ALTER TABLE `permisos`
  MODIFY `id_permiso` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT de la tabla `ranking`
--
ALTER TABLE `ranking`
  MODIFY `id_ranking` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `resultados`
--
ALTER TABLE `resultados`
  MODIFY `id_resultado` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `roles`
--
ALTER TABLE `roles`
  MODIFY `id_rol` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `torneos`
--
ALTER TABLE `torneos`
  MODIFY `id_torneo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `api_tokens`
--
ALTER TABLE `api_tokens`
  ADD CONSTRAINT `api_tokens_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `historial_elo`
--
ALTER TABLE `historial_elo`
  ADD CONSTRAINT `historial_elo_ibfk_1` FOREIGN KEY (`id_jugador`) REFERENCES `jugadores` (`id_jugador`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `historial_elo_ibfk_2` FOREIGN KEY (`id_resultado`) REFERENCES `resultados` (`id_resultado`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Filtros para la tabla `inscripciones`
--
ALTER TABLE `inscripciones`
  ADD CONSTRAINT `inscripciones_ibfk_1` FOREIGN KEY (`id_torneo`) REFERENCES `torneos` (`id_torneo`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `inscripciones_ibfk_2` FOREIGN KEY (`id_jugador`) REFERENCES `jugadores` (`id_jugador`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `jugadores`
--
ALTER TABLE `jugadores`
  ADD CONSTRAINT `jugadores_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `mensajes`
--
ALTER TABLE `mensajes`
  ADD CONSTRAINT `mensajes_ibfk_1` FOREIGN KEY (`id_remitente`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `mensajes_ibfk_2` FOREIGN KEY (`id_destinatario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `ranking`
--
ALTER TABLE `ranking`
  ADD CONSTRAINT `ranking_ibfk_1` FOREIGN KEY (`id_jugador`) REFERENCES `jugadores` (`id_jugador`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `resultados`
--
ALTER TABLE `resultados`
  ADD CONSTRAINT `resultados_ibfk_1` FOREIGN KEY (`id_torneo`) REFERENCES `torneos` (`id_torneo`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `resultados_ibfk_2` FOREIGN KEY (`id_jugador1`) REFERENCES `jugadores` (`id_jugador`) ON UPDATE CASCADE,
  ADD CONSTRAINT `resultados_ibfk_3` FOREIGN KEY (`id_jugador2`) REFERENCES `jugadores` (`id_jugador`) ON UPDATE CASCADE,
  ADD CONSTRAINT `resultados_ibfk_4` FOREIGN KEY (`id_ganador`) REFERENCES `jugadores` (`id_jugador`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Filtros para la tabla `rol_permisos`
--
ALTER TABLE `rol_permisos`
  ADD CONSTRAINT `rol_permisos_ibfk_1` FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id_rol`) ON DELETE CASCADE,
  ADD CONSTRAINT `rol_permisos_ibfk_2` FOREIGN KEY (`id_permiso`) REFERENCES `permisos` (`id_permiso`) ON DELETE CASCADE;

--
-- Filtros para la tabla `torneos`
--
ALTER TABLE `torneos`
  ADD CONSTRAINT `torneos_ibfk_1` FOREIGN KEY (`id_creador`) REFERENCES `usuarios` (`id_usuario`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Filtros para la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD CONSTRAINT `fk_usuario_rol` FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id_rol`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
