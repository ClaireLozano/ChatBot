
 Ce projet vise à créer un chatbot simple qui sera en mesure de :
- réduire le temps passé à répondre à des questions "basiques" d'utilisateurs
- tout en conservant une qualité de réponse acceptable

Il s'agira de trouver une mesure efficace pour associer une question d'utilisateur avec la réaction (réponse) adéquate. Plus exactement, cette mesure doit pouvoir trouver les meilleures réactions (réponse textuelle ou renvoi vers un humain à qui on indique le thème de la question).
 Votre système a le droit de répondre "je ne sais pas" (mais pas trop souvent) et de renvoyer la balle à un humain au hasard. Nous souhaitons un résultat plus efficace que la simple définition manuelle de mots-clés ou de règles.

 Plus formellement, votre chatbot devra prendre en entrée une question utilisateur et fournir en sortie une série de réactions ordonnées par pertinence. Il est à noter que nous ne nous intéresserons pas à la partie purement conversationnelle (Bonjour, comment allez vous, quelles est votre question ...".

 Vous utiliserez les données détaillées ci-dessous pour entrainer votre système à identifier les termes importants (déclencheurs)et à trouver la réaction adaptée. Il vous faudra donc une mesure numérique permettant de mesurer l'adéquation entre une question utilisateur et une série de réactions possibles. Votre mesure d'adéquation pourra éventuellement prévoir une valeur limite en dessous de laquelle le système préférera répondre "Je ne sais pas" et passera la main à un humain chargé de répondre à sa place (en ayant si possible identifié le thème de la question, cf. description du cas d'utilisation 3).

Vous serez confronté à trois cas d'utilisations:
- dans le premier vous aurez une toute petite FAQ de 5 questions. Ceci vous permettra d'exprimer de premières hypothèses
- dans le second vous aurez une liste de 42 questions réponses.
- dans le troisième, fortement doté en ressources contient une FAQ, un log de conversations avec des utilisateurs et une série de questions tests à associer avec des réponses.

 Le cœur de votre chatbot devra être rigoureusement le même pour les trois cas d'utilisation. C'est à dire que votre système ne doit pas être "ad hoc" à un cas d'utilisation. Il apprendra à trouver les bons indices (ou déclencheurs) pour calculer une mesure d'adéquation entre les questions et les réponses quelque soit le domaine fourni en entrée. Vous pourrez par contre différencier votre manière d'extraire les indices et de les pondérer selon que les données viennent de FAQ (plus structurées) ou de questions utilisateurs (où les questions peuvent être plus vagues).
NB : On ne vous demande pas de reformuler les réponses. Il vous est possible par contre de donner simplement des extraits d'une réponse existante si c'est plus pertinent.

Votre code devra:
- utiliser des ressources (FAQ et/ou questions réponses) pour apprendre les termes importants ou "déclencheurs" (mots, groupes de mots, chaînes de caractères...) pour un domaine donné. Vous pouvez utiliser des ressources externes (dictionnaires, corpus ...)
- définir une mesure d'association (de 0 = 'aucun lien' à 1 = 'adéquation parfaite' utilisant ces déclencheurs pour évaluer l'adéquation entre une questions et une réponses
- proposer une fonction prenant en entrée une question donnant en sortie une série ordonnée de réponse de la plus pertinente à la moins pertinente.

Dans votre rendu vous donnerez également un fichier JSON qui à chaque question du fichier "3_questions_syp.json" associera une série de réactions (3 maximum, réponse textuelle ou renvoi à un humain) ordonnées par adéquation décroissante. Pour que le chatbot soit efficace, vous le paramétrez de telle manière qu'il ne réponde "je ne sais pas" dans moins de 15% des cas.

------
Cas d'utilisation 1
1_faq_dmc.json
  fichier de FAQ de la société "Dans ma culotte"


------
Cas d'utilisation 2
2_questions_sorbonne.json
  échanges d'étudiants avec le service des inscriptions de l'université Paris-Sorbonne

------
Cas d'utilisation 3
3_faq_syp.json
  fichier de FAQ de la société "SeeYou-Pub"
3_syp.json
  échanges avec clients de la société SeeYou-Pub
  contenu: liste de conversations par mail ou facebook
  format: pour chaque clé, une liste d'échanges dont le premier est toujours la demande du client.
  réponses: les réponses peuvent être un "texte" ou bien un renvoi vers un service particulier:
    >conseiller/XXX ou XXX est la thématique (connexion, photos ...)
    >message:YYY ou YYY est un message prédéfini
  anonymat: les noms de personnes ont été remplacés par XXX, les pseudos des utilisateurs par PSEUDO
3_questions_syp.json
  liste de questions d'utilisateurs à associer avec une réponse adéquate
