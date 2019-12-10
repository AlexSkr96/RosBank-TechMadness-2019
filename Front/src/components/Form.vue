<template>
  <v-col class="d-flex" cols="6">
    <v-card
      width="100%"
      class="mx-auto pa-5"
    >
      <v-form
        ref="form"
      >
        <v-text-field
          v-model="topic"
          label="Ваша тема"
          required
        />

        <v-select
          :items="operations"
          item-text="name"
          item-value="id"
          return-object
          label="Выберите тип операции"
          @change="pickOperations"
        />

        <div class="chips-wrapper" v-if="assumptionOperations.length != 0">
          <v-hover 
            v-slot:default="{ hover }" 
            v-for="(item, index) in assumptionOperations"
            :key="index"
            open-delay="150"
          >
            <v-chip 
              class="ma-2"
              close
              :color="hover ? '#e60028' : 'grey lighten-2'"
              outlined
              @click="pickedAssumptionChips(item)"
              @click:close="removeAssumptionChips(item)"
            >
              <v-icon left>mdi-fire</v-icon>
              {{ item.name }}
            </v-chip>
          </v-hover>
        </div>

        <div class="chips-wrapper" v-if="pickedOperations.length != 0">
          <v-chip 
            class="ma-2"
            close
            color="red darken-3"
            outlined
            v-for="(item, index) in pickedOperations"
            :key="index"
            @click:close="removeChips(item)"
          >
            <v-icon left>mdi-fire</v-icon>
            {{ item.name }}
          </v-chip>
        </div>

        <v-textarea
          v-model="text"
          outlined
          name="input-7-4"
          label="Ваш текст"
          no-resize
        />

        <vue-dropzone
          ref="myVueDropzone"
          :include-styling="true"
          :useCustomSlot="true"
          id="dropzone"
          @vdropzone-upload-progress="uploadProgress"
          :options="dropzoneOptions"
          @vdropzone-file-added="fileAdded"
          @vdropzone-error-multiple="error"
          @vdropzone-success-multiple="success"
        >
          <div class="dropzone-container">
            <div class="file-selector" v-if="notFile">
              Перетащите файл для загрузки
              <p class="separator"><span> или </span></p>
              <button type="button">выберите файл из проводника</button>
            </div>
            <div class="file-selector" v-else>
              <div class="chips-wrapper" v-if="listUploaderFiles.length != 0">
                <v-chip 
                  class="ma-2"
                  close
                  color="red darken-3"
                  outlined
                  v-for="(item, index) in listUploaderFiles"
                  :key="index"
                  @click:close="removeChipsUpload(item)"
                >
                  <v-icon left>mdi-fire</v-icon>
                  {{ item }}
                </v-chip>
              </div>
            </div>
          </div>
        </vue-dropzone>

        <v-btn
          color="primary"
          class="my-2"
        >
          Отправить
        </v-btn>
      </v-form>
    </v-card>
  </v-col>
</template>

<script>
/* eslint-disable no-alert, no-console, no-unused-vars */
  import vue2Dropzone from "vue2-dropzone"
  import "../../node_modules/vue2-dropzone/dist/vue2Dropzone.min.css"
  import axios from 'axios'

  export default {
    name: 'cForm',
    components: {
      vueDropzone: vue2Dropzone
    },
    data() {
      return {
        notFile: true,
        showForm: false,
        listUploaderFiles: [],
        topic: '',
        text: '',
        tempAttachments: [],
        attachments: [],
        dropzoneOptions: {
          url: `http://localhost:5000/upload`,
          maxFilesize: 102400000,
          paramName: function(n) {
            return "file";
          },
          dictDefaultMessage: "Загрузить файлы здесь",
          includeStyling: false,
          previewsContainer: false,
          thumbnailWidth: 250,
          thumbnailHeight: 140,
          uploadMultiple: true,
          parallelUploads: 20
        },
        assumptionOperations: [],
        pickedOperations: [],
        operations: [{
          id: 0,
          name: 'Кредитование'
        }, {
          id: 1,
          name: 'Депозиты'
        }, {
          id: 2,
          name: 'Валютный контроль'
        }, {
          id: 3,
          name: 'Карты'
        }, {
          id: 4,
          name: 'ЗП'
        }, {
          id: 5,
          name: 'ВЖП'
        }, {
          id: 6,
          name: 'Техническая поддержка'
        }]
      }
    },
    props: {},
    computed: {
      presetUser() {
        return this.$store.getters.getPresetUser
      },
      allOperations() {
        return this.$store.getters.getAllOperations
      }
    },
    watch: {
      presetUser(v) {
        if (v != undefined) {
          this.showForm = true
          this.listUploaderFiles = []
          this.topic = ''
          this.text = ''
          this.assumptionOperations = []
          this.pickedOperations = []
        } else {
          this.showForm = false
        }
      },
      topic(v) {
        // console.log(v)
        if (v != '') { 
          this.sendTextToServer(v, true)
        } else {
          this.operations = this.allOperations
          this.assumptionOperations = []
        }
      },
      text(v) {
        if (v != '') {
          this.sendTextToServer(v, false)
        } else {
          this.operations = this.allOperations
          this.assumptionOperations = []
        }
      }
    },
    created() {
      this.listUploaderFiles = []
      this.topic = ''
      this.text = ''
      this.assumptionOperations = []
      this.pickedOperations = []
    },
    mounted() {},
    methods: {
      sendTextToServer(text, type) {
          axios({
            method: 'get',
            url: `http://localhost:5000/score_text/${text}/${type}`
          })
            .then(result => {
              console.log(result.data)
              this.assumptionOperations = []
              result.data.forEach(item => {
                if (item.value > 0) {
                  this.assumptionOperations.push({
                    id: null,
                    name: item.name,
                    value: item.value
                  })
                }
              })

              this.assumptionOperations.forEach(item => {
                this.operations.forEach(items => {
                  if (item.name === items.name) {
                    item.id = items.id
                  }
                })
              })           

              this.assumptionOperations.sort((a, b) => {
                return b.value - a.value
              })

              // console.log(this.assumptionOperations)

              this.assumptionOperations = this.assumptionOperations.filter((item, index) => {
                return index <= 1
              })

              this.operations = this.allOperations

              // this.assumptionOperations.forEach(item => {
              //   this.operations = this.operations.filter(operations => {
              //     return item.id != operations.id
              //   })
              // })

              // console.log(this.assumptionOperations)

              // res(result.data)
            })
            .catch(err => {
              console.log('Ошибка:')
              console.log(err)
              // rej(err)
            })
        // })
      },
      // function called for every file dropped or selected
      fileAdded(file) {
        console.log("Файл добавлен => ", file)
        this.listUploaderFiles.push(file.name)

        // let attachment = {}
        // attachment._id = file.upload.uuid
        // attachment.title = file.name
        // attachment.type = "file"
        // attachment.extension = "." + file.type.split("/")[1]
        // attachment.user = JSON.parse(localStorage.getItem("user"))
        // attachment.content = "Загрузка файла по выбору или Drag and drop"
        // attachment.thumb = file.dataURL
        // attachment.thumb_list = file.dataURL
        // attachment.isLoading = true
        // attachment.progress = null
        // attachment.size = file.size
        // this.tempAttachments = [...this.tempAttachments, attachment]
        
        // this.loading = true
      },
         // function where we get the upload progress
      uploadProgress(file, progress, bytesSent) {
        // console.log("Ход Загрузки Файлов", progress)
        // this.tempAttachments.map(attachment => {
        //   if (attachment.title === file.name) {
        //     attachment.progress = `${Math.floor(progress)}`
        //   }
        // });
      },
      error(files, message, xhr) {
        // console.log(message.status)
        // console.log(message)
        // console.log(xhr)
      },
      // called on successful upload of a file
      success(file, response) {
        console.log("Файл успешно загружен ")
        console.log("Ответ ->", JSON.parse(response))
        this.notFile = false

        console.log(JSON.parse(response))

        this.assumptionOperations = []
              JSON.parse(response).forEach(item => {
                if (item.value > 0) {
                  this.assumptionOperations.push({
                    id: null,
                    name: item.name,
                    value: item.value
                  })
                }
              })

              this.assumptionOperations.forEach(item => {
                this.operations.forEach(items => {
                  if (item.name === items.name) {
                    item.id = items.id
                  }
                })
              })           

              this.assumptionOperations.sort((a, b) => {
                return b.value - a.value
              })

              console.log(this.assumptionOperations)

              this.assumptionOperations = this.assumptionOperations.filter((item, index) => {
                return index <= 1
              })

              this.operations = this.allOperations

              // this.assumptionOperations.forEach(item => {
              //   this.operations = this.operations.filter(operations => {
              //     return item.id != operations.id
              //   })
              // })

              console.log(this.assumptionOperations)

        

        // this.$refs.myVueDropzone.removeAllFiles()
      },
      pickOperations(item) {
        this.pickedOperations.push(item)

        this.operations = this.operations.filter(operation => {
          return item.id != operation.id
        })
        // console.log(item)
      },
      removeChips(item) {
        this.operations.push(item)
        this.operations.sort((a, b) => {
          return a.id - b.id
        })

        this.pickedOperations = this.pickedOperations.filter(pickedOperations => {
          return item.id != pickedOperations.id
        })
        // console.log(item)
      },
      removeChipsUpload(item) {
        this.listUploaderFiles = this.listUploaderFiles.filter(uploadFile => {
          return item.id != uploadFile.id
        })
        if (this.listUploaderFiles.length === 0) this.notFile = true
      },
      pickedAssumptionChips(item) {
        this.pickedOperations.push(item)

        this.assumptionOperations = this.assumptionOperations.filter(assumptionOperations => {
          return item.id != assumptionOperations.id
        })
      },
      removeAssumptionChips(item) {

        this.operations.push(item)
        this.operations.sort((a, b) => {
          return a.id - b.id
        })

        this.assumptionOperations = this.assumptionOperations.filter(assumptionOperations => {
          return item.id != assumptionOperations.id
        })
      }
    }
  }
</script>
<style>
#dropzone .file-selector {
  padding: .5rem;
  font-weight: 600;
  background-color: #f9f9f9;
  color: #4e5b69;
}
#dropzone figure {
  margin: 0px;
}
#dropzone .dropzone-container {
  display: flex;
  flex-direction: column;
  border: 1px dashed #ccc;
  border-radius: 15px;
}
.dropzone {
  padding: 0
}
#dropzone h1,
h2 {
  font-weight: normal;
}
#dropzone ul {
  list-style-type: none;
  padding: 0;
}
#dropzone li {
  display: inline-block;
  margin: 0 10px;
}
#dropzone a {
  color: #42b983;
}
#dropzone button {
  background: #031629;
  box-shadow: 0 0 2px 0 rgba(3, 22, 41, 0.11),
    0 6px 16px 0 rgba(3, 22, 41, 0.08);
  font-family: SFProDisplay-Regular;
  font-size: 14px;
  color: #ffffff;
  letter-spacing: 0.4px;
  padding: 12px 30px;
  border-radius: 4px;
}
#dropzone .separator {
  position: relative;
}
#dropzone .separator:after {
  position: absolute;
  content: "";
  height: 1px;
  width: 200px;
  background: #d8d8d8;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
#dropzone span {
  position: relative;
  background: #f9f9f9;
  padding: 0 4px;
  /* z-index: 9; */
  font-size: 12px;
  color: #4e5b69;
}
#dropzone .dz-message {
  margin: .5rem 0
}
#dropzone .containerLoading {
  display: -webkit-box;
  display: -webkit-flex;
  display: -ms-flexbox;
  display: flex;
  position: fixed;
  /* z-index: 1060; */
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  -webkit-box-orient: horizontal;
  -webkit-box-direction: normal;
  -webkit-flex-direction: row;
  -ms-flex-direction: row;
          flex-direction: row;
  -webkit-box-align: center;
  -webkit-align-items: center;
  -ms-flex-align: center;
          align-items: center;
  -webkit-box-pack: center;
  -webkit-justify-content: center;
  -ms-flex-pack: center;
          justify-content: center;
  padding: .625em;
  background-color: transparent;
  -webkit-overflow-scrolling: touch;
  background-color: rgba(0,0,0,.4);
  -webkit-transition: background-color .1s;
  -o-transition: background-color .1s;
  transition: background-color .1s;
  align-items: center;
  -webkit-tap-highlight-color: transparent;
  margin-top: 0px!important;
  pointer-events: none;
}
</style>