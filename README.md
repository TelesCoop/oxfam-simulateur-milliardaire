# Oxfam empreinte bouses carbone de l'épargne

## Développer localement

`make serve`

## Mise en production

- `make deploy` va mettre en place le frontend
- pour mettre à jour l'image Amazon lambda, après avoir lancé la commande précédente,
  - choisir nouveau nom du tag, ici `0.0.xxxx`
  - `aws ecr get-login-password --region eu-west-3 | docker login --username AWS --password-stdin 686377688897.dkr.ecr.eu-west-3.amazonaws.com`
  - `docker build -t oxfam-bouses-images .`
  - `docker tag oxfam-bouses-images:latest 686377688897.dkr.ecr.eu-west-3.amazonaws.com/oxfam-bouses-images:0.0.xxxx`
  - `docker push 686377688897.dkr.ecr.eu-west-3.amazonaws.com/oxfam-bouses-images:0.0.xxxx`
  - depuis la console aws, sur la [page de la fonction lambda](https://eu-west-3.console.aws.amazon.com/lambda/home?region=eu-west-3#/functions/oxfamMegaBousesImage?newFunction=true&tab=testing), mettre à jour l'URL de l'image avec donc comme cible `686377688897.dkr.ecr.eu-west-3.amazonaws.com/oxfam-bouses-images:0.0.xxxx`

## Outils utilisés

- CSS: [min](https://github.com/owenversteeg/min)
- JS: [JavaScript-Templates](https://github.com/blueimp/JavaScript-Templates#usage)


## installation https

Suivre les instructions [ici](https://certbot.eff.org/lets-encrypt/ubuntufocal-nginx).
