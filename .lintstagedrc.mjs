export default {
  'data/json/schemas/common.json': (files) => files.map((file) => `ajv compile --spec=draft2020 -s ${file}`),
  'data/json/schemas/{guideline,check,faq}.json': (files) => files.map((file) => `ajv compile --spec=draft2020 -s ${file} -r data/json/schemas/common.json`),
  'data/yaml/gl/**/*.yaml': (files) => files.map((file) => `ajv validate --spec=draft2020 -s data/json/schemas/guideline.json -r data/json/schemas/common.json -d ${file}`),
  'data/yaml/checks/**/*.yaml': (files) => files.map((file) => `ajv validate --spec=draft2020 -s data/json/schemas/check.json -r data/json/schemas/common.json -d ${file}`),
  'data/yaml/faq/**/*.yaml': (files) => files.map((file) => `ajv validate --spec=draft2020 -s data/json/schemas/faq.json -r data/json/schemas/common.json -d ${file}`),
}
