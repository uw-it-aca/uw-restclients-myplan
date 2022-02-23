from commonconf import override_settings

fdao_myplan_override = override_settings(
    RESTCLIENTS_MYPLAN_DAO_CLASS='Mock')
fdao_myplan_auth_override = override_settings(
    RESTCLIENTS_MYPLAN_AUTH_DAO_CLASS='Mock')
