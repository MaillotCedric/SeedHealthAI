# Project template : Vue

Template for Vue projects.

The template is based on Vue.js and allows you to rapidly create a front-end web app.

This template uses [Vuetify](https://vuetifyjs.com/en/).

> Vuetify : a collection of pre-made components paired with powerful features

## Setting up the repository

- Choose a new repository name

- Use it to rename the current cloned repository

- Delete the current `.git` folder (the folder might be hidden)

- Update `README.md`

- Run the following command in the terminal of the repository :

  ```git
  git init
  git add .
  git commit -m "<commit message>"
  ```

*You are now ready to install the project. :)*

## Installation

``` powershell
npm install
npm run format
```

### Compile and Hot-Reload for Development

``` powershell
npm run dev
```

## Compile and Minify for Production

``` powershell
npm run build
```

## Run Unit Tests with [Vitest](https://vitest.dev/)

``` powershell
npm run test:unit
```

## Run End-to-End Tests with [Cypress](https://www.cypress.io/)

``` powershell
npm run test:e2e:dev
```

This runs the end-to-end tests against the Vite development server. It is much faster than the production build.

But it's still recommended to test the production build with `test:e2e` before deploying (e.g. in CI environments) :

``` powershell
npm run build
npm run test:e2e
```

## Lint with [ESLint](https://eslint.org/)

``` powershell
npm run lint
```

