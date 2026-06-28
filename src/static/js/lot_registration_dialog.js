/**
 * ロット登録・編集ダイアログ Alpine.js コンポーネント
 * window.__lotForm にサーバーが初期値を注入する（編集時）
 * window.__lotMode に "new" | "edit" が入る
 */
function lotDialog() {
  return {
    mode: window.__lotMode || "new",

    form: {
      id: "",
      farm_name: "",
      house_number: "",
      crop_type: "",
      crop_variety: "",
      plant_count: "",
    },

    init() {
      // 編集時は window.__lotForm から初期値をセット
      if (window.__lotForm) {
        this.form = {
          id: window.__lotForm.id || "",
          farm_name: window.__lotForm.farm_name || "",
          house_number: window.__lotForm.house_number || "",
          crop_type: window.__lotForm.crop_type || "",
          crop_variety: window.__lotForm.crop_variety || "",
          plant_count:
            window.__lotForm.plant_count != null
              ? String(window.__lotForm.plant_count)
              : "",
        };
      }
    },

    // Alpine.js は Object.defineProperty の get を正しくプロキシしないため
    // getter ではなくメソッドとして定義する
    isEdit() {
      return this.mode === "edit";
    },

    dialogTitle() {
      return this.mode === "edit" ? "ロットを編集" : "ロットを登録";
    },

    primaryLabel() {
      return this.mode === "edit" ? "保存" : "登録";
    },

    close() {
      // 親コンポーネントにダイアログを閉じるよう通知する
      window.dispatchEvent(new CustomEvent("dialog-close"));
    },

    async submit() {
      const formData = new FormData();
      formData.append("lot_id", this.form.id);
      formData.append("farm_name", this.form.farm_name);
      formData.append("house_number", this.form.house_number);
      formData.append("crop_type", this.form.crop_type);
      if (this.form.crop_variety) {
        formData.append("crop_variety", this.form.crop_variety);
      }
      if (this.form.plant_count) {
        formData.append("plant_count", this.form.plant_count);
      }

      const url = this.isEdit()
        ? `/lots/${this.form.id}/update`
        : "/lots";

      const res = await fetch(url, { method: "POST", body: formData });

      // HX-Redirect ヘッダに従って遷移する
      const redirect = res.headers.get("HX-Redirect");
      if (redirect) {
        window.location.href = redirect;
      }
    },

    async deleteLot() {
      if (!confirm("このロットとすべての日報を削除します。よろしいですか？")) return;
      const res = await fetch(`/lots/${this.form.id}/delete`, {
        method: "POST",
      });
      const redirect = res.headers.get("HX-Redirect");
      if (redirect) {
        window.location.href = redirect;
      } else {
        window.location.href = "/";
      }
    },
  };
}
