-- Table des utilisateurs
CREATE TABLE utilisateurs (
    id SERIAL PRIMARY KEY,
    nom_utilisateur VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    mot_de_passe VARCHAR(255) NOT NULL,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des profils utilisateurs
CREATE TABLE profils (
    id_utilisateur INTEGER PRIMARY KEY REFERENCES utilisateurs(id),
    url_avatar VARCHAR(255),
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_mise_a_jour TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des problèmes/questions
CREATE TABLE problemes (
    id SERIAL PRIMARY KEY,
    id_utilisateur INTEGER REFERENCES utilisateurs(id) NULL,
    titre VARCHAR(255) NOT NULL,
    contenu TEXT NOT NULL,
    est_anonyme BOOLEAN DEFAULT FALSE,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_mise_a_jour TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Table des réponses aux problèmes
CREATE TABLE reponses (
    id SERIAL PRIMARY KEY,
    id_probleme INTEGER REFERENCES problemes(id),
    id_utilisateur INTEGER REFERENCES utilisateurs(id),
    contenu TEXT NOT NULL,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_mise_a_jour TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des j'aime pour les problèmes
CREATE TABLE reactionproblemes (
    id SERIAL PRIMARY KEY,
    id_probleme INTEGER REFERENCES problemes(id),
    id_utilisateur INTEGER REFERENCES utilisateurs(id),
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des j'aime pour les réponses
CREATE TABLE reactionreponses (
    id SERIAL PRIMARY KEY,
    id_reponse INTEGER REFERENCES reponses(id),
    id_utilisateur INTEGER REFERENCES utilisateurs(id),
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des notifications
CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    id_utilisateur INTEGER REFERENCES utilisateurs(id),
    message TEXT NOT NULL,
    lu BOOLEAN DEFAULT FALSE,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des conversations
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    id_participant1 INTEGER REFERENCES utilisateurs(id),
    id_participant2 INTEGER REFERENCES utilisateurs(id),
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des messages
CREATE TABLE mess (
    id SERIAL PRIMARY KEY,
    id_conversation INTEGER REFERENCES conversations(id),
    id_expediteur INTEGER REFERENCES utilisateurs(id),
    contenu TEXT NOT NULL,
    horodatage TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);