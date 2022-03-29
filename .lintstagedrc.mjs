export default {
  'data/json/schema/*.json': (files) => files.map((file) => `ajv compile --spec=draft2020 -s ${file}`),
  'data/yaml/gl/**/*.yaml': (files) => files.map((file) => `ajv validate --spec=draft2020 -s data/json/schema/guideline.json -d ${file}`),
  'data/yaml/checks/**/*.yaml': (files) => files.map((file) => `ajv validate --spec=draft2020 -s data/json/schema/check.json -d ${file}`),
}
