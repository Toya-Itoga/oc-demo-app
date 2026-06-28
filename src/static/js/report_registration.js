/**
 * 日報作成画面 Alpine.js コンポーネント
 * window.__reportData にサーバーが既存レポートの初期値を注入する（当日分がある場合）
 * window.__lotId にロットIDを注入する
 */
function reportForm() {
  return {
    lotId: window.__lotId || "",
    plantCondition: 3,
    pestCondition: 5,
    comment: "",
    // 写真: {url, file, name, isExisting, path}
    photos: [],
    submitting: false,

    init() {
      const data = window.__reportData;
      if (data) {
        this.plantCondition = data.plant_condition || 3;
        this.pestCondition = data.pest_condition || 5;
        this.comment = data.comment || "";
        // 既存写真をセット
        const paths = data.photo_paths ? JSON.parse(data.photo_paths) : [];
        this.photos = paths.map((p) => ({
          url: "/" + p,
          file: null,
          name: p.split("/").pop(),
          isExisting: true,
          path: p,
        }));
      }
    },

    /* 評価スライダー */
    setPlant(n) { this.plantCondition = n; },
    setPest(n)  { this.pestCondition = n; },

    plantFill() {
      return ((this.plantCondition - 1) / 4) * 100 + "%";
    },

    pestFill() {
      return ((this.pestCondition - 1) / 4) * 100 + "%";
    },

    stepClass(val, n) {
      if (n === val) return "rating__step rating__step--selected";
      if (n < val)  return "rating__step rating__step--on";
      return "rating__step";
    },

    /* 写真管理 */
    get canAddPhoto() {
      return this.photos.length < 3;
    },

    openFilePicker() {
      this.$refs.fileInput.click();
    },

    handleFiles(e) {
      const files = Array.from(e.target.files);
      for (const file of files) {
        if (this.photos.length >= 3) break;
        this.photos.push({
          url: URL.createObjectURL(file),
          file: file,
          name: file.name,
          isExisting: false,
          path: null,
        });
      }
      // 同じファイルを再選択できるようリセット
      e.target.value = "";
    },

    removePhoto(index) {
      const p = this.photos[index];
      if (!p.isExisting) {
        URL.revokeObjectURL(p.url);
      }
      this.photos.splice(index, 1);
    },

    /* フォーム送信 */
    async submit() {
      if (this.submitting) return;
      this.submitting = true;
      try {
        const fd = new FormData();
        fd.append("plant_condition", String(this.plantCondition));
        fd.append("pest_condition", String(this.pestCondition));
        fd.append("comment", this.comment || "");

        for (const p of this.photos) {
          if (p.isExisting) {
            fd.append("existing_paths", p.path);
          } else {
            fd.append("photos", p.file, p.name);
          }
        }

        const res = await fetch(`/lots/${this.lotId}/report`, {
          method: "POST",
          body: fd,
        });
        const data = await res.json();
        if (data.redirect) {
          window.location.href = data.redirect;
        }
      } catch (err) {
        console.error("保存エラー:", err);
        this.submitting = false;
      }
    },
  };
}
